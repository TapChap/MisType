import json

with open('phrase_dict.json', 'r', encoding='utf-8') as file:
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
    with open('phrase_dict.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(saved_dict))

def reset():
    c_file = open('phrase_dict.json', 'w')
    saved_dict = {}
    c_file.write('{}')
    c_file.close()

if __name__ == '__main__':
    add('aasdfds', 'zcvsvdv')
    print(get())
