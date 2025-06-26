import subprocess, threading, time, sys, os, winreg, app
import tkinter as tk

from tkinter import ttk
from pystray import Icon, Menu, MenuItem
from PIL import Image
from win11toast import toast

# Global variable to track the app process
app_process = None
app_running = False

def get_image():
    try:
        return Image.open(os.path.join(sys._MEIPASS, 'translate_icon.ico'))
    except AttributeError:
        return Image.open('../translate_icon.ico')

def start_app_process():
    """Start the app.py process"""
    global app_process, app_running
    try:
        if getattr(sys, 'frozen', False):
            # When running as exe, app.py is bundled inside the exe
            # We cannot separate them, so we'll run the app logic in the same process
            # This means we need to use threading instead of separate processes

            # Start app in a separate thread instead of separate process
            app_thread = threading.Thread(target=app.main, daemon=True)
            app_thread.start()
            app_running = True
            return True

        else:
            # If running as Python script - separate processes work fine
            app_script = os.path.join(os.path.dirname(__file__), 'app.py')
            app_process = subprocess.Popen([sys.executable, app_script])
            app_running = True
            return True

    except Exception as e:
        print(f"Failed to start app process: {e}")
        return False
def stop_app_process():
    """Stop the app.py process"""
    global app_process, app_running

    if getattr(sys, 'frozen', False):
        # For exe (threading approach)
        try:
            app.quit()  # Call your app's quit function
            app_running = False
        except Exception as e:
            print(f"Error stopping app thread: {e}")
    else:
        # For Python script (subprocess approach)
        if app_process:
            try:
                app_process.terminate()
                app_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                app_process.kill()
            except Exception as e:
                print(f"Error stopping app process: {e}")
            finally:
                app_process = None
                app_running = False

def restart_app(icon):
    """Restart the app process"""
    icon.notify('Restarting application...', title="🔄 Restart")

    if getattr(sys, 'frozen', False):
        # For exe - restart the entire exe since we can't restart just the thread cleanly
        try:
            exe_path = sys.executable
            subprocess.Popen([exe_path])
            time.sleep(1)
            os._exit(0)
        except Exception as e:
            icon.notify(f'Restart failed: {str(e)}', title="❌ Error")
    else:
        # For Python script - use process restart
        stop_app_process()
        time.sleep(0.5)

        if start_app_process():
            icon.notify('Application restarted successfully!', title="✅ Restart")
        else:
            icon.notify('Failed to restart application', title="❌ Error")

def check_app_status():
    """Monitor the app process and restart if it crashes"""
    global app_process, app_running
    while True:
        if app_running and app_process:
            if app_process.poll() is not None:  # Process has ended
                print("App process crashed, attempting restart...")
                time.sleep(1)
                start_app_process()
        time.sleep(5)  # Check every 5 seconds

def on_quit(icon):
    """Quit both the app and tray"""
    stop_app_process()
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

    # icon.notify("Press Win + V to access your clipboard history!", title="📋 Clipboard History Enabled")

def open_dictionary():
    app.open_dictionary()

def change_dictionary_hotkey():
    toast(
        "Action not available yet, Coming Soon!",
        "Current hotkey: Alt + Shift + Q",
        duration="short",  # or 'long'
    )

def setup_tray():
    icon = Icon("MisType")
    icon.icon = get_image()
    icon.menu = Menu(
        MenuItem('Refresh Keybindings', restart_app, default=True),
        Menu.SEPARATOR,
        MenuItem('Change MisType hotkey', change_mistype_hotkey),
        MenuItem('Open Clipboard (Copy History)', enable_clipboard_history),
        MenuItem('Open Dictionary File', open_dictionary),
        Menu.SEPARATOR,
        MenuItem('Quit', on_quit)
    )
    icon.run()

def main():
    # Start the app process
    start_app_process()
    setup_tray()

    # Start monitoring thread
    # monitor_thread = threading.Thread(target=check_app_status, daemon=True)
    # monitor_thread.start()

if __name__ == '__main__':
    main()