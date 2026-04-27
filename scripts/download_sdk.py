"""Download and extract the Wooting RGB SDK to sdk/."""

import os
import sys
import zipfile
import urllib.request

SDK_URL = "https://github.com/WootingKb/wooting-rgb-sdk/releases/download/v1.8.0/wooting-rgb-sdk-v1.8.0-win-x64.zip"
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SDK_DIR = os.path.join(REPO_ROOT, "sdk")
ZIP_PATH = os.path.join(SDK_DIR, "wooting-rgb-sdk.zip")


def download_sdk() -> bool:
    """Download and extract SDK binaries."""
    if os.path.exists(os.path.join(SDK_DIR, "wooting-rgb-sdk64.dll")):
        print("SDK ja esta instalado.")
        return True

    os.makedirs(SDK_DIR, exist_ok=True)

    print("Downloading Wooting RGB SDK v1.8.0...")
    print(f"URL: {SDK_URL}")

    try:
        urllib.request.urlretrieve(SDK_URL, ZIP_PATH, _progress_hook)
        print("\nExtracting SDK archive...")

        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zf.extractall(SDK_DIR)

        os.remove(ZIP_PATH)

        dll_path = os.path.join(SDK_DIR, "wooting-rgb-sdk64.dll")
        if os.path.exists(dll_path):
            print(f"SDK installed at: {SDK_DIR}")
            return True

        for root, _dirs, files in os.walk(SDK_DIR):
            for file_name in files:
                if file_name != "wooting-rgb-sdk64.dll":
                    continue
                src = os.path.join(root, file_name)
                dst = os.path.join(SDK_DIR, file_name)
                if src != dst:
                    os.replace(src, dst)
                print(f"SDK installed at: {SDK_DIR}")
                return True

        print("ERROR: DLL not found after extraction.")
        return False
    except Exception as exc:
        print(f"\nERROR downloading SDK: {exc}")
        print("Download manually from:")
        print(f"  {SDK_URL}")
        print(f"and extract into: {SDK_DIR}")
        return False


def _progress_hook(block_num: int, block_size: int, total_size: int):
    downloaded = block_num * block_size
    if total_size <= 0:
        return
    percent = min(100, downloaded * 100 // total_size)
    bar = "#" * (percent // 2) + "." * (50 - percent // 2)
    sys.stdout.write(f"\r  [{bar}] {percent}%")
    sys.stdout.flush()


if __name__ == "__main__":
    print("=" * 50)
    print("  Wooting RGB SDK Download")
    print("=" * 50)

    if download_sdk():
        print("\nDone.")
    else:
        print("\nFailed.")
