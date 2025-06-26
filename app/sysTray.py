import subprocess, threading, time, sys, os, winreg, app, tempfile
import tkinter as tk

from tkinter import ttk
from pystray import Icon, Menu, MenuItem
from PIL import Image
from win11toast import toast

def get_image():
    try:
        return Image.open(os.path.join(sys._MEIPASS, 'translate_icon.ico'))
    except AttributeError:
        return Image.open('../translate_icon.ico')

def on_quit(icon):
    """Quit both the app and tray"""
    app.quit()
    icon.stop()
    sys.exit()

def change_mistype_hotkey():
    # Run tkinter in main thread
    def create_text_field():
        def on_submit(event=None):
            key = entry.get().strip().lower()
            if len(key) == 1 and key.isalnum():
                modifiers = []
                if ctrl_var.get(): modifiers.append("ctrl")
                if alt_var.get(): modifiers.append("alt")
                if shift_var.get(): modifiers.append("shift")
                if win_var.get(): modifiers.append("windows")
                hotkey = "+".join(modifiers + [key])
                app.change_mistype_hotkey(hotkey)
            input_dialog.destroy()
            root.destroy()

        root = tk.Tk()
        root.withdraw()

        input_dialog = tk.Toplevel()
        input_dialog.title("Change Hotkey")
        input_dialog.geometry("320x250")
        input_dialog.configure(bg="#f0f0f0")

        style = ttk.Style()
        style.theme_use("vista")
        style.configure("TCheckbutton", font=('Segoe UI', 10), background="#f0f0f0", padding=6)
        style.configure("TLabel", background="#f0f0f0", font=('Segoe UI', 10))
        style.configure("TButton", font=('Segoe UI', 10))

        label = ttk.Label(input_dialog, text="Select modifiers:")
        label.pack(pady=(15, 5))

        # Checkboxes for modifiers
        ctrl_var = tk.BooleanVar()
        alt_var = tk.BooleanVar()
        shift_var = tk.BooleanVar()
        win_var = tk.BooleanVar()

        checkbox_frame = ttk.Frame(input_dialog)
        checkbox_frame.pack()

        ttk.Checkbutton(checkbox_frame, text="Ctrl", variable=ctrl_var).grid(row=0, column=0, padx=10, pady=5)
        ttk.Checkbutton(checkbox_frame, text="Alt", variable=alt_var).grid(row=0, column=1, padx=10, pady=5)
        ttk.Checkbutton(checkbox_frame, text="Shift", variable=shift_var).grid(row=1, column=0, padx=10, pady=5)
        ttk.Checkbutton(checkbox_frame, text="Win", variable=win_var).grid(row=1, column=1, padx=10, pady=5)

        key_label = ttk.Label(input_dialog, text="Enter single key (a–z, 0–9):")
        key_label.pack(pady=(15, 5))

        entry = ttk.Entry(input_dialog, width=10, font=('Segoe UI', 12))
        entry.pack()

        submit_btn = ttk.Button(input_dialog, text="Submit", command=on_submit)
        submit_btn.pack(pady=15)

        entry.bind("<Return>", on_submit)
        input_dialog.protocol("WM_DELETE_WINDOW", root.quit)

        # Center on screen without `eval` (which is not available on Toplevel)
        input_dialog.update_idletasks()
        root.mainloop()

    threading.Thread(target=create_text_field).start()

def enable_clipboard_history():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Microsoft\Clipboard", 0, winreg.KEY_SET_VALUE)
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Clipboard")

    winreg.SetValueEx(key, "EnableClipboardHistory", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)

    app.app_open_clipboard()

def open_dictionary():
    app.open_dictionary()

def change_dictionary_hotkey():
    toast(
        "Action not available yet, Coming Soon!",
        "Current hotkey: Alt + Shift + Q",
        duration="short",
    )

def setup_tray():
    icon = Icon("MisType")
    icon.icon = get_image()
    icon.menu = Menu(
        # MenuItem('Refresh Keybindings', restart_app, default=True),
        # Menu.SEPARATOR,
        MenuItem('Change MisType hotkey', change_mistype_hotkey),
        MenuItem('Open Clipboard (Copy History)', enable_clipboard_history),
        MenuItem('Open Dictionary File', open_dictionary),
        Menu.SEPARATOR,
        MenuItem('Quit', on_quit)
    )
    icon.run()

def main():
    # Start the app process
    app.main()
    setup_tray()

if __name__ == '__main__':
    main()