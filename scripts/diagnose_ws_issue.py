#!/usr/bin/env python3
"""
WootFlow WebSocket Diagnostic Script
Verifica porta 9120, logs, prerequisites, e conectividade local.
"""

import os
import sys
import socket
import json
import subprocess
import urllib.request
import urllib.error
import time

def check_port_9120_in_use() -> bool:
    """Verifica se a porta 9120 já está em uso."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 9120))
        sock.close()
        return result == 0  # 0 = porta em uso
    except Exception as e:
        print(f"[!] Erro ao verificar porta: {e}")
        return False


def check_health_endpoint(timeout: float = 5.0) -> bool:
    """Tenta conectar ao endpoint /health do WootFlow."""
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:9120/health",
            headers={"Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            ok = payload.get("ok")
            service = payload.get("service")
            if ok and service == "WootFlow":
                return True
            else:
                print(f"[!] Health check resposta inválida: ok={ok}, service={service}")
                return False
    except urllib.error.URLError as e:
        print(f"[!] Health check falhou: {e.reason}")
        return False
    except Exception as e:
        print(f"[!] Health check erro: {e}")
        return False


def check_logs() -> str:
    """Encontra e lê o arquivo de log mais recente."""
    local_appdata = os.environ.get("LOCALAPPDATA")
    candidates = []

    if local_appdata:
        candidates.append(os.path.join(local_appdata, "WootFlow", "logs", "wootflow_debug.log"))

    candidates.append(os.path.join(os.path.dirname(__file__), "..", "wootflow_debug.log"))
    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wootflow_debug.log"))

    for path in candidates:
        if os.path.exists(path):
            print(f"[✓] Log encontrado: {path}\n")
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()[-30:]  # últimas 30 linhas
                    return "".join(lines)
            except Exception as e:
                print(f"[!] Erro ao ler log: {e}")
                return f"Erro ao ler {path}"

    return "[!] Nenhum arquivo de log encontrado"


def check_vcredist() -> bool:
    """Verifica VC++ Redistributable."""
    if sys.platform != "win32":
        return True
    try:
        import winreg
        paths = [
            r"SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
            r"SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
        ]
        for path in paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    installed, _ = winreg.QueryValueEx(key, "Installed")
                    major, _ = winreg.QueryValueEx(key, "Major")
                    if int(installed) == 1 and int(major) >= 14:
                        return True
            except OSError:
                continue
    except Exception:
        pass
    return False


def check_webview2() -> bool:
    """Verifica WebView2 Runtime."""
    if sys.platform != "win32":
        return True
    try:
        import winreg
        keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
        ]
        for hive, path in keys:
            try:
                with winreg.OpenKey(hive, path) as key:
                    version, _ = winreg.QueryValueEx(key, "pv")
                    if version:
                        return True
            except OSError:
                continue
    except Exception:
        pass
    return False


def main():
    print("=" * 70)
    print("WootFlow WebSocket Diagnostic")
    print("=" * 70)
    print()

    # 1. Checks de Port
    print("[1] Verificando porta 9120...")
    if check_port_9120_in_use():
        print("[✗] CRÍTICO: Porto 9120 JÁ EM USO")
        print("    Ação: Fechar outro processo ou mudar a porta em main_desktop.py:_start_server()")
    else:
        print("[✓] Porto 9120 está livre")
    print()

    # 2. Health endpoint
    print("[2] Tentando conectar a http://127.0.0.1:9120/health...")
    if check_health_endpoint(timeout=3.0):
        print("[✓] Health endpoint respondeu correctamente")
        print("    ✓ Servidor está OK, problema pode ser no front-end (React hook)")
    else:
        print("[✗] Health endpoint NÃO respondeu")
        print("    ✗ Servidor pode estar crash ou não iniciado")
    print()

    # 3. Logs
    print("[3] Verificando logs...")
    log_content = check_logs()
    print(log_content)
    print()

    # 4. Prerequisites
    print("[4] Verificando Prerequisites Windows...")
    vc_ok = check_vcredist()
    wv2_ok = check_webview2()
    
    if sys.platform == "win32":
        if vc_ok:
            print("[✓] Visual C++ Redistributable x64 instalado")
        else:
            print("[✗] Visual C++ Redistributable x64 NÃO encontrado")
            print("    Ação: Instale via: https://support.microsoft.com/en-us/help/2977003")
        
        if wv2_ok:
            print("[✓] WebView2 Runtime instalado")
        else:
            print("[✗] WebView2 Runtime NÃO encontrado")
            print("    Ação: Instale via: https://developer.microsoft.com/en-us/microsoft-edge/webview2/")
    else:
        print("[✓] Sistema não-Windows (skipped)")
    print()

    print("=" * 70)
    print("Próximos passos:")
    print("=" * 70)
    print()
    print("1. Se porta 9120 está em uso:")
    print("   netstat -ano | findstr :9120")
    print("   taskkill /PID <pid> /F")
    print()
    print("2. Se health endpoint não responde:")
    print("   - Verifica os ERROS no log acima")
    print("   - Se houver erro de SDK/USB, reconecta o keyboard")
    print("   - Se houver erro de módulo Python, reinstala via install_all.ps1")
    print()
    print("3. Se health responde mas app fica em 'loading':")
    print("   - Problema está no lado do front-end (React)")
    print("   - Verifica browser console (F12) para erros JS")
    print()


if __name__ == "__main__":
    main()
