from pystray import Icon, Menu, MenuItem
from PIL import Image
from win11toast import toast
from tkinter import messagebox, ttk
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
        root.withdraw()  # Hide the main root window

        # Setup dialog
        input_dialog = tk.Toplevel()
        input_dialog.title("Change Hotkey")
        input_dialog.geometry("320x260")
        input_dialog.resizable(False, False)

        # Use ttk style for modern appearance
        style = ttk.Style()
        style.theme_use('clam')  # Modern look; try 'vista', 'alt', or 'clam'

        main_frame = ttk.Frame(input_dialog, padding=20)
        main_frame.pack(fill='both', expand=True)

        # Title
        ttk.Label(main_frame, text="Customize Hotkey", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))

        # Modifier checkboxes
        ttk.Label(main_frame, text="Select modifier keys:").pack(anchor='w')

        modifiers = {
            "ctrl": tk.BooleanVar(),
            "alt": tk.BooleanVar(),
            "shift": tk.BooleanVar(),
            "windows": tk.BooleanVar()
        }

        check_frame = ttk.Frame(main_frame)
        check_frame.pack(anchor='w', pady=5)

        for key, var in modifiers.items():
            ttk.Checkbutton(check_frame, text=key.capitalize(), variable=var).pack(side='left', padx=5)

        # Key entry
        ttk.Label(main_frame, text="\nEnter the main key:").pack(anchor='w')
        key_entry = ttk.Entry(main_frame, width=5, justify="center", font=("Segoe UI", 10))
        key_entry.pack(pady=(0, 10))

        # Submit function
        def on_submit():
            key = key_entry.get().lower().strip()
            if not key or len(key) != 1:
                messagebox.showerror("Invalid Input", "Please enter a single character (e.g., 'z').")
                return

            hotkey_parts = [k for k, v in modifiers.items() if v.get()]
            hotkey_parts.append(key)
            hotkey_str = " + ".join(hotkey_parts)
            app.change_hotkey(hotkey_str)
            input_dialog.destroy()
            root.destroy()

        # Submit button
        ttk.Button(main_frame, text="Apply Hotkey", command=on_submit).pack(pady=10)

        # Bind enter key
        input_dialog.bind("<Return>", lambda e: on_submit())

        # Clean exit
        input_dialog.protocol("WM_DELETE_WINDOW", root.quit)
        # Center the Toplevel window manually
        input_dialog.update_idletasks()
        w = input_dialog.winfo_width()
        h = input_dialog.winfo_height()
        x = (input_dialog.winfo_screenwidth() // 2) - (w // 2)
        y = (input_dialog.winfo_screenheight() // 2) - (h // 2)
        input_dialog.geometry(f"+{x}+{y}")
        input_dialog.mainloop()


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
        MenuItem('Change MisType hotkey', changeHotkey),
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
