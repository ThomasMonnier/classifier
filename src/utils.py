from . import convert_from_path, os, pd, pytesseract, st


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


def highlight_suppliers(series):
    green = "background-color: aquamarine"
    very_red = "background-color: tomato"
    red = "background-color: mistyrose"
    return [very_red if v == "UNKNOWN" else red if v is None else green for v in series]


def highlight_language(series):
    green = "background-color: aquamarine"
    very_red = "background-color: tomato"
    red = "background-color: mistyrose"
    return [
        red if 50 < int(v) < 70 else very_red if int(v) <= 50 else green for v in series
    ]


def highlight_type(series):
    green = "background-color: aquamarine"
    orange = "background-color: bisque"
    red = "background-color: mistyrose"
    return [
        orange if v == "To be checked" else red if v is None else green for v in series
    ]
