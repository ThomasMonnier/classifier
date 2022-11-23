import os
import shutil

import pandas as pd
import streamlit as st

from src.clf_country import detect_lang_from_str
from src.clf_provider_contract import (find_contract_from_invoice,
                                       find_provider_from_invoice)
from src.clf_supplier import load_model, prepare_img
from src.utils import action, convert_pdf, ocr_tesseract

dict_labels = {
    0: "Endesa",
    1: "Energia xxi",
    2: "Fenie",
    3: "Holaluz",
    4: "Iberdrola",
    5: "Naturgy",
}

df_countries = pd.read_csv(
    "languages.csv", header=None, names=["abreviation", "country"]
)
dict_countries = dict(zip(df_countries.abreviation, df_countries.country))


def classifier_country(ocr_str):
    """Invoice Language"""
    lng, prob = detect_lang_from_str(ocr_str)
    return lng, img_path, prob


def classifier_supplier(model_path, img_path, lng, model_use=True, stats_use=True):
    """Invoice Supplier"""
    model_pred, stats_pred = None, None
    if model_use:
        model = load_model(model_path)
        img_final = prepare_img(img_path)
        model_pred = model.predict([img_final])

    if stats_use:
        df_providers = pd.read_csv("classifier_rules/{}_provider.csv".format(lng))
        dico_provider = {
            df_providers[column].name: [
                y.lower() for y in df_providers[column] if not pd.isna(y)
            ]
            for column in df_providers
        }
        stats_pred = find_provider_from_invoice(ocr_str.lower(), dico_provider)

    return model_pred, stats_pred


def classifier_type(ocr_str, lng):
    """Invoice Energy Type"""
    df_contracts = pd.read_csv(
        "classifier_rules/{}_contract.csv".format(lng),
        skiprows=[0, 1],
        names=[
            "Electricity_+",
            "Gas_+",
            "Heat_+",
            "Other_+",
            "Electricity_-",
            "Gas_-",
            "Heat_-",
            "Other_-",
        ],
    )
    dico_contracts = {
        df_contracts[column].name: [
            y.lower() for y in df_contracts[column] if not pd.isna(y)
        ]
        for column in df_contracts
    }
    energy_type, message = find_contract_from_invoice(ocr_str.lower(), dico_contracts)
    return energy_type, message


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classifier API</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "With this API, you can import an invoice (PDF or PNG) which will be first classified by its country, then by its supplier, and then by its energy type."
    )

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=[
                "File",
                "Language",
                "Language Probability",
                "Type",
                "Type Probability",
                "Supplier (ML)",
                "Supplier (Stats)",
                "Supplier (Mindee)",
            ]
        )

    uploaded_files = st.file_uploader(
        "Choose a file (PDF / PNG)",
        type=["png", "jpg", "pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        progress_bar = st.progress(0)

        dataframe = st.dataframe(st.session_state.df)

        for i, uploaded_file in enumerate(uploaded_files):
            if uploaded_file.name not in list(st.session_state.df["File"]):
                st.session_state.df.loc[i] = [
                    uploaded_file.name,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                ]

                with open(uploaded_file.name, "wb") as buffer:
                    shutil.copyfileobj(uploaded_file, buffer)

                img_path = convert_pdf(uploaded_file.name)
                ocr_str = ocr_tesseract(img_path)

                # Language
                lng, img_path, prob = classifier_country(ocr_str)
                st.session_state.df.loc[
                    st.session_state.df["File"] == uploaded_file.name, "Language"
                ] = dict_countries.get(lng)
                st.session_state.df.loc[
                    st.session_state.df["File"] == uploaded_file.name,
                    "Language Probability",
                ] = int(100 * prob)
                dataframe.dataframe(st.session_state.df)

                # Type
                if lng in ["es", "fr", "it"]:
                    energy_type, message = classifier_type(ocr_str, lng)
                    st.session_state.df.loc[
                        st.session_state.df["File"] == uploaded_file.name, "Type"
                    ] = energy_type
                    st.session_state.df.loc[
                        st.session_state.df["File"] == uploaded_file.name,
                        "Type Probability",
                    ] = message
                    dataframe.dataframe(st.session_state.df)

                # Supplier
                if lng in ["es", "ca"]:
                    model_path = "models/spain_supplier_model.pkl"
                    model_pred, stats_pred = classifier_supplier(
                        model_path, img_path, "es"
                    )
                    st.session_state.df.loc[
                        st.session_state.df["File"] == uploaded_file.name,
                        "Supplier (ML)",
                    ] = dict_labels.get(model_pred[0]).upper()
                    st.session_state.df.loc[
                        st.session_state.df["File"] == uploaded_file.name,
                        "Supplier (Stats)",
                    ] = stats_pred.upper()
                    dataframe.dataframe(st.session_state.df)

                elif lng in ["fr", "it"]:
                    model_path = "models/spain_supplier_model.pkl"
                    _, stats_pred = classifier_supplier(model_path, img_path, lng)
                    st.session_state.df.loc[
                        st.session_state.df["File"] == uploaded_file.name,
                        "Supplier (Stats)",
                    ] = stats_pred.upper()
                    dataframe.dataframe(st.session_state.df)

            progress_bar.progress(int(100 * (i + 1) / len(uploaded_files)))

        st.session_state.df.to_csv("results.csv")

        if os.path.isfile("results.csv"):
            with open("results.csv", "rb") as csv_file:
                col1, col2, col3 = st.columns(3)
                with col2:
                    st.download_button(
                        label="Download data as a CSV file",
                        data=csv_file,
                        mime="application/csv",
                        file_name="results.csv",
                        on_click=action,
                    )
