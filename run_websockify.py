import shutil
import subprocess
import sys

WS_PORT = "8181"
TARGET = "127.0.0.1:9339"


def is_installed() -> bool:
    return shutil.which("websockify") is not None


def install() -> bool:
    print("websockify not found.")
    answer = input("Install it now via pip? (y/n): ").strip().lower()
    if answer != "y":
        print("Cannot continue without websockify. Exiting.")
        return False

    print("Installing websockify...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "websockify", "--break-system-packages"],
            check=True,
        )
    except subprocess.CalledProcessError:
        print("Installation failed. Try installing manually:")
        print("  pip install websockify --break-system-packages")
        return False

    if not is_installed():
        print("websockify still not found on PATH after installation.")
        print("You may need to restart your terminal.")
        return False

    print("websockify installed successfully.")
    return True


def run():
    print(f"Starting websockify: {WS_PORT} -> {TARGET}")
    try:
        subprocess.run(["websockify", WS_PORT, TARGET])
    except KeyboardInterrupt:
        print("\nwebsockify stopped.")


if __name__ == "__main__":
    if not is_installed():
        if not install():
            sys.exit(1)
    run()
