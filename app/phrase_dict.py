import json, os

json_path = os.path.join(os.getenv('APPDATA'), 'MisType', 'saved_dict.json')

# Ensure directory exists
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# initialize file if needed
if not os.path.exists(json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({"initialize": 'init'}, f, indent=2)

def __get_dict():
    with open(json_path, 'r', encoding='utf-8') as file:
       _dict = json.load(file)
    return _dict

def __update_dict(_dict):
    if not _dict:
        raise FileNotFoundError('key or value missing in update_dict method')

    _current = __get_dict()
    _current.update(_dict)
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump(_current, file)

def reset():
    with open(json_path, 'w', encoding='utf-8') as file:
        json.dump({}, file)

def get(key=''):
    saved_dict = __get_dict()

    if not key:
        return saved_dict

    if key not in saved_dict.keys():
        return None
    return saved_dict[key]

def add(key, val):
    __update_dict({key: val})

if __name__ == '__main__':
    print(get())
