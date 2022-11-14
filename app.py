import shutil
import pandas as pd

import streamlit as st

from src.clf_country import detect_lang_from_str
from src.clf_supplier import load_model, prepare_img
from src.utils import convert_pdf, ocr_tesseract

dict_labels = {
    0: "endesa",
    1: "energia_xxi",
    2: "fenie",
    3: "holaluz",
    4: "iberdrola",
    5: "naturgy",
}

df = pd.read_csv('languages.csv', header=None, names=['abreviation', 'country'])
dict_countries = dict(zip(df.abreviation, df.country))


def classifier_country(file):
    img_path = convert_pdf(file)
    ocr_str = ocr_tesseract(img_path)
    lng, prob = detect_lang_from_str(ocr_str)
    st.info('Probability info: {}%'.format(round(prob * 100, 2)))
    st.success("Country: {}".format(dict_countries.get(lng)))
    return lng, img_path


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

    uploaded_file = st.file_uploader(
        "Choose a file (PDF / PNG)",
    )

    if uploaded_file:
        with open(uploaded_file.name, "wb") as buffer:
            shutil.copyfileobj(uploaded_file, buffer)
        
        if 'lng' not in st.session_state:
            st.session_state['lng'] = None
        if 'img_path' not in st.session_state:
            st.session_state['img_path'] = None

        _, lng_api, _ = st.columns(3)
        with lng_api:
            lng_api_button = st.button("Get the language of file", key="clf_1")

        if lng_api_button:
            st.session_state['lng'], st.session_state['img_path'] = classifier_country(uploaded_file.name)
            st.image(st.session_state['img_path'])
        
        if st.session_state['lng'] == "es":
            _, supp_api, _ = st.columns(3)
            with supp_api:
                supp_api_button = st.button("Get the supplier", key="clf_2")
            if supp_api_button:
                model_path = "models/spain_supplier_model.pkl"
                pred = classifier_supplier(model_path, st.session_state['img_path'])
                st.info("Supplier is {}".format(dict_labels[pred[0]]))
