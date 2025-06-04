import time, pyperclip, string_converter, os
import keyboard as kb

from pynput.keyboard import Key, Controller

global hotkey

# available hotkey keys:
# ctrl, alt, shift, windows
# Letter keys: a–z
# Special keys: enter, esc, space, tab, backspace, up, down, left, right, etc.

def waitUntilRelease(key):
    while kb.is_pressed(key):
        time.sleep(0.01)


def handle_hotkey(keyboard):

    keys = hotkey.split('+')
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
    kb.write(string_converter.convert(text))

    # change pc language
    kb.press_and_release('alt + shift')

def change_hotkey(new_hotkey):
    global hotkey
    hotkey = new_hotkey

    kb.unhook_all()
    kb.add_hotkey(new_hotkey, lambda: handle_hotkey(Controller()))

def quit():
    kb.unhook_all()
    os._exit(0)
    exit(0)

def main():
    global hotkey
    hotkey = 'alt+shift+z'

    kb.add_hotkey(hotkey, lambda: handle_hotkey(Controller()))
    kb.wait()

if __name__ == '__main__':
    main()