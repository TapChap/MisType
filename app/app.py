import time, pyperclip, os
import keyboard as kb
import string_converter, phrase_dict

from pynput.keyboard import Key, Controller
from lang_helper import get_sys_lang

global mistype_hotkey, dictionary_hotkey

def waitUntilRelease(key):
    if type(key) is not list:
        while kb.is_pressed(key):
            time.sleep(0.01)
        return

    for k in key:
        while kb.is_pressed(k):
            time.sleep(0.01)

def handle_mistype_hotkey(keyboard):
    print('mistype hotkey detected')

    keys = mistype_hotkey.split('+')
    for key in keys:
        waitUntilRelease(key)

    # using a different lib to handle shift & home keystrokes
    # since keyboard package couldn't do it
    keyboard.press(Key.shift)
    keyboard.press(Key.home)

    keyboard.release(Key.shift)
    keyboard.release(Key.home)

    # cut the bad text
    kb.press_and_release('ctrl + x')
    time.sleep(0.05)

    # convert the bad text to the correct language and paste it
    text = pyperclip.paste()
    print(text)
    kb.write(string_converter.convert(text))

    # change pc language
    kb.press_and_release('alt + shift')

def change_mistype_hotkey(new_hotkey):
    global mistype_hotkey
    mistype_hotkey = new_hotkey

    kb.unhook_all()
    kb.add_hotkey(new_hotkey, lambda: handle_mistype_hotkey(Controller()))

# -------------

def app_open_clipboard():
    kb.press_and_release('win + v')

# -------------
def handle_dictionary_hotkey(keyboard):
    keys = dictionary_hotkey.split('+')
    waitUntilRelease(keys)

    # select the last word
    dir, direction = ('l', 'left') if get_sys_lang() == 'en' else ('r', 'right')
    print(direction)

    # align the textbox to the correct alignment
    keyboard.press(eval(f"Key.ctrl_{dir}"))
    keyboard.press(eval(f"Key.shift_{dir}"))
    time.sleep(0.05)

    keyboard.release(eval(f"Key.ctrl_{dir}"))
    keyboard.release(eval(f"Key.shift_{dir}"))
    time.sleep(0.05)

    # copy the last written word
    keyboard.press(Key.ctrl)
    keyboard.press(Key.shift)

    keyboard.tap(eval(f"Key.{direction}"))
    time.sleep(0.05)

    keyboard.release(Key.ctrl)
    keyboard.release(Key.shift)

    # cut the word and re-write it
    kb.press_and_release('ctrl + x')
    time.sleep(0.05)

    text = pyperclip.paste()
    print(text)
    dict_text = phrase_dict.get(text)

    if not dict_text:
        kb.write(text)
    else:
        kb.write(dict_text)

def open_dictionary():
    os.startfile(phrase_dict.json_path)

# -------------

def quit():
    """Clean shutdown"""
    kb.unhook_all()
    os._exit(0)

def main():
    global mistype_hotkey, dictionary_hotkey

    mistype_hotkey = 'alt+shift+z'
    dictionary_hotkey = 'alt+shift+q'

    kb.add_hotkey(dictionary_hotkey, lambda: handle_dictionary_hotkey(Controller()))
    kb.add_hotkey(mistype_hotkey, lambda: handle_mistype_hotkey(Controller()))

    kb.wait()

if __name__ == '__main__':
    main()