"""
Script para baixar automaticamente o Wooting RGB SDK.
"""

import os
import sys
import zipfile
import urllib.request

SDK_URL = "https://github.com/WootingKb/wooting-rgb-sdk/releases/download/v1.8.0/wooting-rgb-sdk-v1.8.0-win-x64.zip"
SDK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sdk")
ZIP_PATH = os.path.join(SDK_DIR, "wooting-rgb-sdk.zip")


def download_sdk():
    """Baixa e extrai o Wooting RGB SDK automaticamente."""
    if os.path.exists(os.path.join(SDK_DIR, "wooting-rgb-sdk64.dll")):
        print("SDK já está instalado!")
        return True

    os.makedirs(SDK_DIR, exist_ok=True)

    print(f"Baixando Wooting RGB SDK v1.8.0...")
    print(f"URL: {SDK_URL}")
    print()

    try:
        urllib.request.urlretrieve(SDK_URL, ZIP_PATH, _progress_hook)
        print("\n\nExtraindo...")

        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zf.extractall(SDK_DIR)

        # Remove o zip
        os.remove(ZIP_PATH)

        # Verifica se a DLL foi extraída
        dll_path = os.path.join(SDK_DIR, "wooting-rgb-sdk64.dll")
        if os.path.exists(dll_path):
            print(f"SDK instalado com sucesso em: {SDK_DIR}")
            return True

        # Pode estar em uma subpasta
        for root, dirs, files in os.walk(SDK_DIR):
            for f in files:
                if f == "wooting-rgb-sdk64.dll":
                    # Move para a raiz do sdk/
                    src = os.path.join(root, f)
                    dst = os.path.join(SDK_DIR, f)
                    if src != dst:
                        os.rename(src, dst)
                    print(f"SDK instalado com sucesso em: {SDK_DIR}")
                    return True

        print("ERRO: DLL não encontrada após extração.")
        return False

    except Exception as e:
        print(f"\nERRO ao baixar o SDK: {e}")
        print(f"\nBaixe manualmente de:")
        print(f"  {SDK_URL}")
        print(f"E extraia na pasta: {SDK_DIR}")
        return False


def _progress_hook(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, downloaded * 100 // total_size)
        bar = "█" * (percent // 2) + "░" * (50 - percent // 2)
        sys.stdout.write(f"\r  [{bar}] {percent}%")
        sys.stdout.flush()


if __name__ == "__main__":
    print("=" * 50)
    print("  Wooting RGB SDK - Setup")
    print("=" * 50)
    print()

    success = download_sdk()

    if success:
        print("\nTudo pronto! Execute: python main.py")
    else:
        print("\nFalha na instalação. Veja o README.md.")

    input("\nPressione Enter para sair...")
