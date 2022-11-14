import shutil
import pandas as pd

import streamlit as st

from src.clf_country import detect_lang_from_str
from src.clf_supplier import load_model, prepare_img
from src.utils import convert_pdf, ocr_tesseract

dict_labels = {
    0: "Endesa",
    1: "Energia xxi",
    2: "Fenie",
    3: "Holaluz",
    4: "Iberdrola",
    5: "Naturgy",
}

df_countries = pd.read_csv('languages.csv', header=None, names=['abreviation', 'country'])
dict_countries = dict(zip(df_countries.abreviation, df_countries.country))


def classifier_country(file):
    img_path = convert_pdf(file)
    ocr_str = ocr_tesseract(img_path)
    lng, prob = detect_lang_from_str(ocr_str)
    return lng, img_path, prob


def classifier_supplier(model_path, img_path):
    model = load_model(model_path)
    img_final = prepare_img(img_path)
    pred = model.predict([img_final])
    return pred


def classifier_type():
    pass


if __name__ == "__main__":
    st.markdown(
        "<h1 style='text-align: center; color: green;'>Classifier API</h1>",
        unsafe_allow_html=True,
    )
    st.write(
        "With this API, you can import an invoice (PDF or PNG) which will be first classified by its country, then by its supplier, and then by its energy type."
    )

    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=["File", "Language", "Language Probability", "Supplier (ML)", "Supplier (Mindee)", "Supplier (Stats)"])

    uploaded_files = st.file_uploader(
        "Choose a file (PDF / PNG)",
        type=['png', 'jpg', 'pdf'],
        accept_multiple_files=True
    )

    placeholder = st.empty()

    with placeholder.container():

        if uploaded_files:

            for i, uploaded_file in enumerate(uploaded_files):
                st.session_state.df.loc[i] = [uploaded_file.name, None, None, None, None, None]

                with open(uploaded_file.name, "wb") as buffer:
                    shutil.copyfileobj(uploaded_file, buffer)

                lng, img_path, prob = classifier_country(uploaded_file.name)
                st.session_state.df.loc[st.session_state.df['File'] == uploaded_file.name, 'Language'] = dict_countries.get(lng)
                st.session_state.df.loc[st.session_state.df['File'] == uploaded_file.name, 'Language Probability'] = round(100 * prob, 2)
                
                if lng == "es":
                    model_path = "models/spain_supplier_model.pkl"
                    pred = classifier_supplier(model_path, img_path)
                    st.session_state.df.loc[st.session_state.df['File'] == uploaded_file.name, 'Supplier (ML)'] = dict_labels.get(pred[0])

            st.dataframe(st.session_state.df)
