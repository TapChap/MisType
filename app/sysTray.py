from pystray import Icon, Menu, MenuItem
from PIL import Image
import tkinter as tk
import threading, sys, app, os

def GetImage():
    path = os.path.join(sys._MEIPASS, 'translate_icon.ico')

    return Image.open(path)

# Quit action
def on_quit(icon, item):
    app.quit()        # Your custom cleanup logic
    icon.stop()
    sys.exit()

# Text input popup
def changeHotkey(icon, item):
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
                app.change_hotkey(" + ".join(text.lower().replace(' ', '').split(',')))
            input_dialog.destroy()
            root.quit()

        submit_btn = tk.Button(input_dialog, text="Submit", command=on_submit)
        submit_btn.pack(pady=10)

        entry.bind("<Return>", on_submit)  # Bind Enter key to submit

        input_dialog.protocol("WM_DELETE_WINDOW", root.quit)
        root.mainloop()

    threading.Thread(target=create_text_field).start()

# Setup tray icon
def setup_tray():
    icon = Icon("MisType")
    icon.icon = GetImage()
    icon.menu = Menu(
        MenuItem('Quit', on_quit),
        MenuItem('Change hotkey', changeHotkey)
    )
    icon.run()

def main():
    # Start tray icon in a background thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    app.main()

if __name__ == '__main__':
    main()
