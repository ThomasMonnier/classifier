from . import pytesseract, convert_from_path, st


def ocr_tesseract(path):
    return pytesseract.image_to_string(path)


def convert_pdf(file):
    if file.name.endswith('.pdf'):
        pages = convert_from_path(file, 500)
        pages[0].save("{}.png".format(file.name.split('.')[0]), 'PNG')
        return "{}.png".format(file.name.split('.')[0])
    
    elif file.name.endswith(".png"):
        return file.name
    
    else:
        st.error('The file is not in PNG nor PDF format.')
