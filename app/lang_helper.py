import ctypes

languages = {
    0x0409: 'en',  # English - United States
    0x040D: 'he'  # Hebrew
}

user32 = ctypes.WinDLL('user32', use_last_error=True)

def get_sys_lang():
    hwnd = user32.GetForegroundWindow()
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    layout_id = user32.GetKeyboardLayout(thread_id)
    lang_id = layout_id & 0xFFFF

    return languages[lang_id]

if __name__ == '__main__':
    while True:
        print(get_sys_lang())