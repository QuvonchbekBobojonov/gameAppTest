import ctypes
import sys
import os


def is_admin():
    """Check if the script is running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if is_admin():
        # Put the code that requires admin privileges here
        print("You are running with administrator privileges.")
        # Example: Accessing protected system directories, modifying registry, etc.
    else:
        # If not running as admin, request elevation
        print("Requesting administrator privileges...")
        # Restart script with admin rights
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, os.path.abspath(__file__), None, 1
        )
