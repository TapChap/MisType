import json, os, sys

try:
    # PyInstaller creates a temp folder and stores the path in _MEIPASS
    base_path = sys._MEIPASS
except AttributeError:
    base_path = os.path.abspath("..")  # fallback when running in development

file_path = os.path.join(base_path, 'phrase_dict.json')

with open(file_path, 'r', encoding='utf-8') as file:
    saved_dict = json.load(file)

def get(key=''):
    if not key:
        return saved_dict

    if key not in saved_dict.keys():
        return None
    return saved_dict[key]

def add(key, val):
    new_dict = {key: val}
    saved_dict.update(new_dict)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(saved_dict))

def reset():
    global saved_dict

    c_file = open('../phrase_dict.json', 'w')
    saved_dict = {}
    c_file.write('{}')
    c_file.close()