import os
import time, pyperclip, string_converter
import keyboard as kb

from pynput.keyboard import Key, Controller

# available hotkey keys:
# ctrl, alt, shift, windows
# Letter keys: a–z
# Special keys: enter, esc, space, tab, backspace, up, down, left, right, etc.

def handle_hotkey(keyboard):
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
    kb.write(string_converter.convert(text))

    # change pc language
    kb.press_and_release('alt + shift')

def change_hotkey(new_hotkey):
    kb.unhook_all()
    kb.add_hotkey(new_hotkey, lambda: handle_hotkey(Controller()))

def quit():
    # kb.press_and_release('esc')
    kb.unhook_all()
    os._exit(0)
    exit(0)

def main():
    kb.add_hotkey('alt + shift + z', lambda: handle_hotkey(Controller()))
    kb.wait()

if __name__ == '__main__':
    main()