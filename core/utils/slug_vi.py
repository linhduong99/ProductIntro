import re

_vietnamese_map = {
    "o": "o", "ò": "o", "ó": "o", "ỏ": "o", "õ": "o", "ọ": "o",
    "ơ": "o", "ờ": "o", "ớ": "o", "ở": "o", "ỡ": "o", "ợ": "o",
    "ô": "o", "ồ": "o", "ố": "o", "ổ": "o", "ỗ": "o", "ộ": "o",
    "a": "a", "à": "a", "á": "a", "ả": "a", "ã": "a", "ạ": "a",
    "ă": "a", "ắ": "a", "ằ": "a", "ẳ": "a", "ẵ": "a", "ặ": "a",
    "â": "a", "ầ": "a", "ấ": "a", "ẩ": "a", "ẫ": "a", "ậ": "a",
    "đ": "d", "Đ": "d",
    "e": "e", "è": "e", "é": "e", "ẻ": "e", "ẽ": "e", "ẹ": "e",
    "ê": "e", "ề": "e", "ế": "e", "ể": "e", "ễ": "e", "ệ": "e",
    "i": "i", "ì": "i", "í": "i", "ỉ": "i", "ĩ": "i", "ị": "i",
    "ư": "u", "ừ": "u", "ứ": "u", "ử": "u", "ữ": "u", "ự": "u",
    "u": "u", "ù": "u", "ú": "u", "ủ": "u", "ũ": "u", "ụ": "u",
    "y": "y", "ỳ": "y", "ý": "y", "ỷ": "y", "ỹ": "y", "ỵ": "y",
}


def slugify(text, join_str='-'):
    if text is None or len(text.strip()) == 0 or join_str is None:
        return None
    text = re.sub(r"[-]+", " ", text)
    text = re.sub(r"[ ]+", " ", text).lower().strip()
    words = text.split(" ")
    new_words = []
    for word in words:
        ws = []
        for w in word:
            if not w.strip():
                continue
            if w in _vietnamese_map.keys():
                ws.append(_vietnamese_map[w])
            else:
                ws.append(w)

        new_words.append(re.sub(r"[^a-zA-Z0-9]", "", "".join(ws)))
    slug = join_str.join(new_words)
    return re.sub(r"[-]+", "-", slug)
