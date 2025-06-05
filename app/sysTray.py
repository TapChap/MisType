from pystray import Icon, Menu, MenuItem
from PIL import Image
from win11toast import toast
import tkinter as tk
import threading, sys, app, os, winreg

def get_image():
    try:
        return Image.open(os.path.join(sys._MEIPASS, 'translate_icon.ico'))
    except AttributeError:
        return Image.open('../translate_icon.ico')

# Quit action
def on_quit(icon):
    app.quit()        # Your custom cleanup logic
    icon.stop()
    sys.exit()

# Text input popup
def changeHotkey():
    # Run tkinter in main thread
    def create_text_field():
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        input_dialog = tk.Toplevel()
        input_dialog.title("MisType")
        input_dialog.geometry("300x120")

        label = tk.Label(input_dialog, text="Enter new hotkey (separated by ','):")
        label.pack(pady=10)

        entry = tk.Entry(input_dialog, width=50)
        entry.pack(padx=20)

        def on_submit(event=None):
            text = entry.get()
            if text:
                app.change_hotkey("+".join(text.lower().replace(' ', '').split(',')))
            input_dialog.destroy()
            root.destroy()

        submit_btn = tk.Button(input_dialog, text="Submit", command=on_submit)
        submit_btn.pack(pady=10)

        entry.bind("<Return>", on_submit)  # Bind Enter key to submit

        input_dialog.protocol("WM_DELETE_WINDOW", root.quit)
        root.mainloop()

    threading.Thread(target=create_text_field).start()

def enable_clipboard_history():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Clipboard", 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Clipboard")

    winreg.SetValueEx(key, "EnableClipboardHistory", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)

    show_clipboard_toast()


def show_clipboard_toast():
    toast(
        "📋 Clipboard History Enabled",
        "Press Win + V to access your clipboard history!",
        duration="short",  # or 'long'
        on_click=app.app_open_clipboard
    )

# Setup tray icon
def setup_tray():
    icon = Icon("MisType")
    icon.icon = get_image()
    icon.menu = Menu(
        MenuItem('Quit', on_quit),
        MenuItem('Change hotkey', changeHotkey),
        MenuItem('Enable clipboard History', enable_clipboard_history)
    )
    icon.run()

def main():
    # Start tray icon in a background thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    app.main()

if __name__ == '__main__':
    main()
