dictionary = {
    # letter to letter
    'a': 'ש',
    'b': 'נ',
    'c': 'ב',
    'd': 'ג',
    'e': 'ק',
    'f': 'כ',
    'g': 'ע',
    'h': 'י',
    'i': 'ן',
    'j': 'ח',
    'k': 'ל',
    'l': 'ך',
    'm': 'צ',
    'n': 'מ',
    'o': 'ם',
    'p': 'פ',
    'r': 'ר',
    's': 'ד',
    't': 'א',
    'u': 'ו',
    'v': 'ה',
    'x': 'ס',
    'y': 'ט',
    'z': 'ז',

    # letter to special chr
    'q': '/',
    'w': "'",
    ',': 'ת',
    ';': 'ף',
    '.': 'ץ',

    # special chr to special chr
    "'": ',',
    "/": '.',
}

ENtoHE = dictionary

# HEtoEN = dict(zip(dictionary.values(), dictionary.keys()))
HEtoEN = {v: k for k, v in dictionary.items()}
