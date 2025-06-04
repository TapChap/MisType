import os
import time, pyperclip, string_converter
import keyboard as kw

from pynput.keyboard import Key, Controller

# available hotkey keys:
# ctrl, alt, shift, windows
# Letter keys: a–z
# Special keys: enter, esc, space, tab, backspace, up, down, left, right, etc.

def handle_hotkey(keyboard):
    time.sleep(0.5)

    # using a different lib to handle shift & home keystrokes
    # since keyboard package couldn't do it
    keyboard.press(Key.shift)
    keyboard.press(Key.home)
    keyboard.release(Key.shift)
    keyboard.release(Key.home)

    # cut the bad text
    kw.press_and_release('ctrl + x')
    time.sleep(0.05)

    # convert the bad to text to the correct language and paste it
    text = pyperclip.paste()
    kw.write(string_converter.convert(text))

    # change pc language
    kw.press_and_release('alt + shift')

def change_hotkey(new_hotkey):
    kw.unhook_all()
    kw.add_hotkey(new_hotkey, lambda: handle_hotkey(Controller()))

def quit():
    # kw.press_and_release('esc')
    kw.unhook_all()
    os._exit(0)
    exit(0)

def main():
    kw.add_hotkey('alt + shift + z', lambda: handle_hotkey(Controller()))
    kw.wait()

if __name__ == '__main__':
    main()