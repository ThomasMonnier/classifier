from . import convert_from_path, os, pytesseract, st


def ocr_tesseract(path):
    return pytesseract.image_to_string(path)


def convert_pdf(file):
    if file.split(".")[-1] == "pdf":
        pages = convert_from_path(file, 500)
        pages[0].save("{}.png".format("".join(file.split(".")[:-1])), "PNG")
        return "{}.png".format("".join(file.split(".")[:-1]))

    elif file.split(".")[-1] == "png":
        return file

    else:
        st.error("The file is not in PNG nor PDF format.")


def action():
    os.remove("results.csv")
