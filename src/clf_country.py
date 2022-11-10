from . import detect


def detect_lang_from_str(ocr_str):
    lines = list(set(ocr_str.split('\n')))
    lines.remove('')
    lines.remove(' ')

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
    
    yield lng
    lng = max(lang, key=lang.get)
    lang_others = lang.copy()
    del lang_others[lng]
    lng_val = lang[lng]
    if lng_val > 2 * lang[max(lang_others, key=lang_others.get)]:
        return lng
    else:
        return None