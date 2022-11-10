import streamlit as st
import shutil

from src.utils import ocr_tesseract, convert_pdf


def classifier_country(uploaded_file):
    _, lng_api, _ = st.columns(3)

    with lng_api:
        lng_api_button = st.button('Get the language of file')

    if lng_api_button:
        img_path = convert_pdf(uploaded_file)
        ocr_str = ocr_tesseract(img_path)
        all_lng, lng = classifier_country(ocr_str)
        if lng is None:
            st.error('Impossible to detect the language of the document, check {}'.format(all_lng))
        else:
            st.info('Country: {}'.format(lng))


def classifier_supplier():
    pass


def classifier_type():
    pass


if __name__=="__main__":
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
        classifier_country(uploaded_file)
