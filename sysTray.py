from pystray import Icon, Menu, MenuItem
from PIL import Image
import tkinter as tk
import threading, sys, app, os

global keyboard_thread

# Create an icon image
def create_image():
    path = os.path.join(sys._MEIPASS, 'translate_icon.ico')

    return Image.open(path)

# Quit action
def on_quit(icon, item):
    global keyboard_thread

    app.quit()        # Your custom cleanup logic
    icon.stop()
    sys.exit()

# Text input popup
def prompt_for_text(icon, item):
    # Run tkinter in main thread
    def run_input():
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        input_dialog = tk.Toplevel()
        input_dialog.title("MisType")

        # Set desired width here (e.g. 400px)
        input_dialog.geometry("400x120")

        label = tk.Label(input_dialog, text="Enter new hotkey (separated by ','):")
        label.pack(pady=10)

        entry = tk.Entry(input_dialog, width=50)
        entry.pack(padx=20)

        def on_submit(event = None):
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

    threading.Thread(target=run_input).start()

# Setup tray icon
def setup_tray():
    icon = Icon("MisType")
    icon.icon = create_image()
    icon.menu = Menu(
        MenuItem('Quit', on_quit),
        MenuItem('Change hotkey', prompt_for_text)
    )
    icon.run()

def main():
    # Start tray icon in a background thread
    tray_thread = threading.Thread(target=setup_tray, daemon=True)
    tray_thread.start()

    app.main()

if __name__ == '__main__':
    main()
