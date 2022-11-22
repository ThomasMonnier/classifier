from . import detect


def detect_lang_from_str(ocr_str):
    lines = list(set(ocr_str.split("\n")))
    try:
        lines.remove("")
    except:
        pass
    try:
        lines.remove(" ")
    except:
        pass

    lang = {}
    for line in lines:
        try:
            lang_detected = detect(line)
            if lang_detected not in lang.keys():
                lang[lang_detected] = 1
            else:
                lang[lang_detected] += 1
        except:
            pass

    lng = max(lang, key=lang.get)
    lang_others = lang.copy()
    del lang_others[lng]
    lng_val = lang[lng]
    if lng_val > 2 * lang[max(lang_others, key=lang_others.get)]:
        prob = 1.0
    else:
        prob = 1 - 0.8 * ((2 * lang[max(lang_others, key=lang_others.get)] - lng_val) / lng_val)
    return lng, prob
