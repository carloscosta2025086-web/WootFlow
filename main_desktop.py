"""
Wooting RGB Desktop — abre a UI numa janela nativa via pywebview.
Inicia o FastAPI server em background e abre a janela apontando para ele.
Este é o entry point para o .exe (PyInstaller).
"""

import sys
import os
import atexit
import threading
import time
import traceback
import logging
import shutil
import subprocess
import json
import tempfile
import urllib.request
import urllib.error
import urllib.parse
import webbrowser

try:
    from app_version import APP_VERSION
except Exception:
    APP_VERSION = "0.0.0-dev"

# Garantir que imports relativos funcionam no PyInstaller
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASE)

def _resolve_log_path() -> str:
    """Escolhe um caminho de log gravável (evita Program Files)."""
    local_appdata = os.environ.get("LOCALAPPDATA")
    candidates = []

    if local_appdata:
        candidates.append(os.path.join(local_appdata, "WootFlow", "logs", "wootflow_debug.log"))

    candidates.append(os.path.join(_BASE, "wootflow_debug.log"))
    candidates.append(os.path.join(tempfile.gettempdir(), "wootflow_debug.log"))

    for path in candidates:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "a", encoding="utf-8"):
                pass
            return path
        except Exception:
            continue

    return os.path.join(tempfile.gettempdir(), "wootflow_debug.log")


_LOG_PATH = _resolve_log_path()
try:
    logging.basicConfig(
        filename=_LOG_PATH,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
except Exception:
    _LOG_PATH = os.path.join(tempfile.gettempdir(), "wootflow_debug.log")
    logging.basicConfig(
        filename=_LOG_PATH,
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        encoding="utf-8",
    )
_log = logging.getLogger("main_desktop")
_log.info("=== WootFlow startup ===")
_log.info("BASE=%s", _BASE)
_log.info("sys.frozen=%s", getattr(sys, 'frozen', False))
_log.info("app_version=%s", APP_VERSION)

_UPDATE_REPO = "carloscosta2025086-web/WootFlow"
_UPDATE_API = f"https://api.github.com/repos/{_UPDATE_REPO}/releases/latest"
_UPDATE_STATE_FILE = os.path.join(os.environ.get("LOCALAPPDATA", _BASE), "WootFlow", "update_state.json")

# Importar server no thread principal para garantir acesso ao cleanup
try:
    import server as _srv
    _log.info("server imported OK")
except Exception as _e:
    _log.exception("FAILED to import server: %s", _e)
    raise


def _start_server():
    """Inicia o FastAPI/uvicorn em background thread."""
    try:
        import uvicorn
        _log.info("uvicorn imported OK, starting on :9120")
        
        # Diagnóstico: verifica se porta já está em uso
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', 9120))
            sock.close()
            if result == 0:
                _log.critical("PORT 9120 ALREADY IN USE by another process!")
                raise RuntimeError("Port 9120 already in use")
        except Exception as _e:
            if "already in use" in str(_e).lower():
                _log.critical("PORT 9120 ALREADY IN USE: %s", _e)
                raise
        
        # Tenta iniciar uvicorn
        _log.info("Starting uvicorn on 127.0.0.1:9120 with log_level=warning")
        uvicorn.run(_srv.app, host="127.0.0.1", port=9120, log_level="warning")
        _log.info("uvicorn exited cleanly")
    except Exception as _exc:
        _log.exception("SERVER CRASHED with exception: %s", _exc)
        _log.error("Full traceback: %s", traceback.format_exc())


def _wait_for_server(timeout: float = 20.0):
    """Espera até o servidor local responder com health válido."""
    _log.info("Waiting for server health check (timeout=%s seconds)...", timeout)
    t0 = time.time()
    attempt = 0
    while time.time() - t0 < timeout:
        attempt += 1
        try:
            req = urllib.request.Request(
                "http://127.0.0.1:9120/health",
                headers={"Accept": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            if payload.get("ok") and payload.get("service") == "WootFlow":
                elapsed = time.time() - t0
                _log.info("✓ Server health OK (took %.1f seconds)", elapsed)
                return True
        except urllib.error.URLError as _e:
            if attempt % 4 == 0:  # Log a cada 1 segundo
                _log.debug("Health check attempt %d failed: %s", attempt, _e.reason)
        except Exception as _e:
            if attempt % 4 == 0:
                _log.debug("Health check attempt %d error: %s", attempt, type(_e).__name__)
        
        time.sleep(0.25)
    
    _log.error("✗ Server health check FAILED after %.1f seconds", timeout)
    return False


def _show_server_start_error() -> None:
    msg = (
        "O servidor local do WootFlow nao arrancou corretamente.\n\n"
        "=== POSSÍVEIS CAUSAS ===\n"
        "1. PORTA 9120 JÁ EM USO:\n"
        "   Outro processo está usando a porta. Verifica com:\n"
        "   netstat -ano | findstr :9120\n\n"
        "2. DEPENDÊNCIAS/RUNTIME FALTANDO:\n"
        "   Executa: install_all.ps1 para reinstalar\n\n"
        "3. SDK WOOTING/USB NÃO RESPONDENDO:\n"
        "   Reconecta o keyboard ou tenta em outro USB\n\n"
        "4. VISUAL C++ REDISTRIBUTABLE:\n"
        "   Download: https://support.microsoft.com/en-us/help/2977003\n\n"
        "=== DIAGNÓSTICO ===\n"
        f"Log: {_LOG_PATH}\n"
        "Script: scripts\\diagnose_ws_issue.py\n\n"
        "Por favor, revê o log acima para erros específicos."
    )
    _log.error("Server health check failed after timeout; aborting UI startup")
    _message_box("WootFlow - Erro de arranque do servidor", msg, 0x00000010)


def _cleanup_sdk():
    """Força cleanup do SDK ao fechar a janela/processo."""
    try:
        _srv._force_cleanup()
    except Exception:
        pass


def _has_vcredist_x64() -> bool:
    """Verifica se o Visual C++ Redistributable x64 (14+) está instalado."""
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
        return False
    return False


def _has_webview2_runtime() -> bool:
    """Verifica se o WebView2 Runtime está instalado."""
    if sys.platform != "win32":
        return True
    try:
        import winreg
        keys = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"),
        ]
        for hive, path in keys:
            try:
                with winreg.OpenKey(hive, path) as key:
                    version, _ = winreg.QueryValueEx(key, "pv")
                    if version:
                        return True
            except OSError:
                continue

        # Fallback: procurar entradas de uninstall (alguns ambientes registam aqui).
        uninstall_roots = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for hive, root in uninstall_roots:
            try:
                with winreg.OpenKey(hive, root) as key:
                    count, _, _ = winreg.QueryInfoKey(key)
                    for i in range(count):
                        sub_name = winreg.EnumKey(key, i)
                        try:
                            with winreg.OpenKey(key, sub_name) as sub:
                                display_name, _ = winreg.QueryValueEx(sub, "DisplayName")
                                if "WebView2 Runtime" in str(display_name):
                                    return True
                        except OSError:
                            continue
            except OSError:
                continue
    except Exception:
        return False
    return False


def _try_install_with_winget(package_id: str, package_name: str) -> bool:
    """Tenta instalar um pacote via winget sem interação do utilizador."""
    winget = shutil.which("winget")
    if not winget:
        _log.warning("winget nao encontrado; nao foi possivel instalar %s", package_name)
        return False

    cmd = [
        winget,
        "install",
        "--id",
        package_id,
        "--exact",
        "--silent",
        "--accept-source-agreements",
        "--accept-package-agreements",
    ]
    _log.info("Instalando pre-requisito via winget: %s (%s)", package_name, package_id)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
        _log.info("winget returncode=%s", result.returncode)
        if result.stdout:
            _log.info("winget stdout: %s", result.stdout[-4000:])
        if result.stderr:
            _log.warning("winget stderr: %s", result.stderr[-4000:])
        return result.returncode == 0
    except Exception as exc:
        _log.exception("Falha ao instalar %s via winget: %s", package_name, exc)
        return False


def _download_and_run_installer(name: str, url: str, silent_args: list[str]) -> bool:
    """Fallback: descarrega instalador oficial e executa em modo silencioso."""
    try:
        installers_dir = os.path.join(os.environ.get("LOCALAPPDATA", _BASE), "WootFlow", "installers")
        os.makedirs(installers_dir, exist_ok=True)
        filename = os.path.basename(urllib.parse.urlparse(url).path) or f"{name}.exe"
        local_installer = os.path.join(installers_dir, filename)

        _log.info("Downloading installer for %s from %s", name, url)
        urllib.request.urlretrieve(url, local_installer)

        cmd = [local_installer, *silent_args]
        _log.info("Running installer for %s: %s", name, cmd)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
        _log.info("Installer %s exit code=%s", name, result.returncode)
        if result.stdout:
            _log.info("%s stdout: %s", name, result.stdout[-3000:])
        if result.stderr:
            _log.warning("%s stderr: %s", name, result.stderr[-3000:])
        return result.returncode == 0
    except Exception as exc:
        _log.exception("Fallback installer failed for %s: %s", name, exc)
        return False


def _ensure_windows_prerequisites():
    """No Windows, verifica e tenta instalar runtimes essenciais em first-run.

    Nota: pode requerer elevacao/UAC dependendo da maquina.
    """
    if sys.platform != "win32":
        return

    missing = []
    if not _has_vcredist_x64():
        missing.append(("Microsoft.VCRedist.2015+.x64", "Visual C++ Redistributable x64"))
    if not _has_webview2_runtime():
        missing.append(("Microsoft.EdgeWebView2Runtime", "Microsoft Edge WebView2 Runtime"))

    if not missing:
        _log.info("Pre-requisitos Windows OK")
        return

    _log.warning("Pre-requisitos em falta: %s", ", ".join([m[1] for m in missing]))

    fallback_map = {
        "Microsoft.VCRedist.2015+.x64": {
            "url": "https://aka.ms/vs/17/release/vc_redist.x64.exe",
            "args": ["/install", "/quiet", "/norestart"],
        },
        "Microsoft.EdgeWebView2Runtime": {
            "url": "https://go.microsoft.com/fwlink/p/?LinkId=2124703",
            "args": ["/silent", "/install"],
        },
    }

    for package_id, package_name in missing:
        installed = _try_install_with_winget(package_id, package_name)
        if installed:
            continue

        fb = fallback_map.get(package_id)
        if not fb:
            continue
        _log.warning("Trying fallback installer for %s", package_name)
        _download_and_run_installer(package_name, fb["url"], fb["args"])

    still_missing = []
    if not _has_vcredist_x64():
        still_missing.append("Visual C++ Redistributable x64")
    if not _has_webview2_runtime():
        still_missing.append("Microsoft Edge WebView2 Runtime")

    if still_missing:
        _log.error("Still missing prerequisites after install attempts: %s", ", ".join(still_missing))


def _parse_version(version_text: str):
    v = (version_text or "").strip().lower()
    if v.startswith("v"):
        v = v[1:]
    parts = []
    for item in v.split("."):
        num = ""
        for ch in item:
            if ch.isdigit():
                num += ch
            else:
                break
        parts.append(int(num) if num else 0)
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts[:3])


def _is_newer_version(latest_tag: str, current_version: str) -> bool:
    return _parse_version(latest_tag) > _parse_version(current_version)


def _ensure_update_state_dir():
    folder = os.path.dirname(_UPDATE_STATE_FILE)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)


def _should_check_updates(interval_hours: int = 12) -> bool:
    try:
        if not os.path.exists(_UPDATE_STATE_FILE):
            return True
        with open(_UPDATE_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        last_check = float(state.get("last_check_epoch", 0))
        return (time.time() - last_check) >= interval_hours * 3600
    except Exception:
        return True


def _mark_update_checked():
    try:
        _ensure_update_state_dir()
        with open(_UPDATE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_check_epoch": time.time()}, f)
    except Exception:
        _log.exception("Falha ao gravar estado de update")


def _message_box(title: str, message: str, flags: int) -> int:
    try:
        import ctypes
        return ctypes.windll.user32.MessageBoxW(None, message, title, flags)
    except Exception:
        return 0


def _fetch_latest_release_info():
    req = urllib.request.Request(
        _UPDATE_API,
        headers={
            "User-Agent": "WootFlow-Updater",
            "Accept": "application/vnd.github+json",
        },
    )
    with urllib.request.urlopen(req, timeout=8) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return {
        "tag_name": payload.get("tag_name", ""),
        "html_url": payload.get("html_url", f"https://github.com/{_UPDATE_REPO}/releases"),
        "assets": payload.get("assets", []) or [],
    }


def _find_installer_asset(assets):
    """Find setup installer asset in release artifacts."""
    preferred = {"wootflow-setup.exe", "wootflowsetup.exe"}

    for asset in assets:
        name = (asset.get("name") or "").strip().lower()
        if name in preferred:
            return asset

    for asset in assets:
        name = (asset.get("name") or "").strip().lower()
        if name.endswith(".exe") and "wootflow" in name and "setup" in name:
            return asset

    return None


def _download_update_exe(asset) -> str:
    url = asset.get("browser_download_url")
    if not url:
        raise RuntimeError("Asset sem URL de download")

    update_dir = os.path.join(os.environ.get("LOCALAPPDATA", _BASE), "WootFlow", "updates")
    os.makedirs(update_dir, exist_ok=True)
    asset_name = (asset.get("name") or "wootflow-setup.exe").strip() or "wootflow-setup.exe"
    temp_path = os.path.join(update_dir, asset_name)

    req = urllib.request.Request(url, headers={"User-Agent": "WootFlow-Updater"})
    with urllib.request.urlopen(req, timeout=60) as resp, open(temp_path, "wb") as out:
        shutil.copyfileobj(resp, out)

    return temp_path


def _run_installer_and_exit(installer_path: str) -> bool:
    """Run installer detached and let the current app exit."""
    if not installer_path or not os.path.exists(installer_path):
        return False

    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    subprocess.Popen(
        [installer_path],
        creationflags=creation_flags,
        close_fds=True,
    )
    return True


def _spawn_updater_and_exit(new_exe_path: str) -> bool:
    if not getattr(sys, "frozen", False):
        return False

    current_exe = sys.executable
    temp_dir = tempfile.gettempdir()
    bat_path = os.path.join(temp_dir, "wootflow_apply_update.bat")

    script = """@echo off
setlocal
set TARGET=%~1
set NEWEXE=%~2
set RETRIES=0

:waitloop
timeout /t 1 /nobreak >nul
move /Y "%NEWEXE%" "%TARGET%" >nul 2>nul
if errorlevel 1 (
  set /a RETRIES+=1
  if %RETRIES% GEQ 30 goto fail
  goto waitloop
)

start "" "%TARGET%"
del "%~f0"
exit /b 0

:fail
start "" https://github.com/carloscosta2025086-web/WootFlow/releases
del "%~f0"
exit /b 1
"""

    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(script)

    creation_flags = 0
    if sys.platform == "win32":
        creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS

    subprocess.Popen(
        ["cmd", "/c", bat_path, current_exe, new_exe_path],
        creationflags=creation_flags,
        close_fds=True,
    )
    return True


def _check_for_updates_and_maybe_apply() -> bool:
    """Retorna True quando o app deve terminar para aplicar atualização."""
    if sys.platform != "win32":
        return False
    if not getattr(sys, "frozen", False):
        return False
    if not _should_check_updates():
        return False

    try:
        release = _fetch_latest_release_info()
    except Exception:
        _log.exception("Falha ao verificar updates")
        return False

    # Only throttle future checks if we could actually reach and parse the
    # release endpoint successfully.
    _mark_update_checked()

    latest_tag = release.get("tag_name", "")
    if not latest_tag or not _is_newer_version(latest_tag, APP_VERSION):
        return False

    MB_YESNO = 0x00000004
    MB_ICONINFORMATION = 0x00000040
    IDYES = 6

    answer = _message_box(
        "WootFlow - Atualizacao Disponivel",
        f"Nova versao disponivel: {latest_tag}\nVersao atual: {APP_VERSION}\n\nDeseja atualizar agora?",
        MB_YESNO | MB_ICONINFORMATION,
    )
    if answer != IDYES:
        return False

    asset = _find_installer_asset(release.get("assets", []))
    if not asset:
        _message_box(
            "WootFlow - Atualizacao",
            "Nao foi encontrado o ficheiro wootflow-setup.exe na release.\nAbrindo pagina de releases.",
            MB_ICONINFORMATION,
        )
        webbrowser.open(release.get("html_url", f"https://github.com/{_UPDATE_REPO}/releases"))
        return False

    try:
        installer_path = _download_update_exe(asset)
        if _run_installer_and_exit(installer_path):
            return True
    except Exception:
        _log.exception("Falha ao aplicar update")
        _message_box(
            "WootFlow - Atualizacao",
            "Falha ao aplicar atualizacao automatica.\nAbrindo pagina de releases.",
            MB_ICONINFORMATION,
        )
        webbrowser.open(release.get("html_url", f"https://github.com/{_UPDATE_REPO}/releases"))

    return False


def main():
    _ensure_windows_prerequisites()

    if _check_for_updates_and_maybe_apply():
        return

    import webview

    # Tray support (optional)
    try:
        import pystray
        from PIL import Image, ImageDraw
        HAS_PYSTRAY = True
    except Exception:
        HAS_PYSTRAY = False

    _tray_icon = None
    _tray_thread = None

    # Registar cleanup para qualquer saída do processo
    atexit.register(_cleanup_sdk)

    # No Windows, capturar CTRL_CLOSE_EVENT (janela a fechar)
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32

            @ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_uint)
            def _console_handler(event):
                # CTRL_CLOSE_EVENT=2, CTRL_LOGOFF_EVENT=5, CTRL_SHUTDOWN_EVENT=6
                if event in (2, 5, 6):
                    _cleanup_sdk()
                return 0

            kernel32.SetConsoleCtrlHandler(_console_handler, True)
            # Keep reference alive
            main._console_handler = _console_handler
        except Exception:
            pass

    # Start server in daemon thread
    server_thread = threading.Thread(target=_start_server, daemon=True)
    server_thread.start()

    # Wait for server to be ready with explicit health validation.
    if not _wait_for_server(timeout=20.0):
        _show_server_start_error()
        return

    # Open native window
    window = webview.create_window(
        title="Wooting RGB",
        url="http://127.0.0.1:9120",
        width=1280,
        height=820,
        min_size=(960, 640),
        background_color="#0a0a0f",
        frameless=False,
        easy_drag=False,
    )

    def on_closing():
        """Chamado quando a janela está a fechar — minimiza para a tray.

        Retorna False para cancelar o fecho (pywebview interpreta um
        retorno False como pedido para cancelar o fecho). Se pystray não
        estiver disponível, faz cleanup e permite fechar.
        """
        # Se não tivermos suporte a tray, prosseguir com cleanup e fechar
        if not HAS_PYSTRAY:
            _cleanup_sdk()
            return True

        # Mostrar só a tray e esconder a janela
        try:
            window.hide()
        except Exception:
            pass

        def _create_tray():
            nonlocal _tray_icon, _tray_thread
            if _tray_icon is not None:
                return

            # Ícone simples (círculo colorido)
            try:
                img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
                draw = ImageDraw.Draw(img)
                draw.ellipse((8, 8, 56, 56), fill=(48, 120, 200))
            except Exception:
                img = None

            def _on_open(icon_obj, item):
                try:
                    # Stop tray and restore window
                    try:
                        icon_obj.stop()
                    except Exception:
                        pass
                    _tray_icon = None
                    _tray_thread = None
                    window.show()
                    window.restore()
                except Exception:
                    pass

            def _on_quit(icon_obj, item):
                try:
                    icon_obj.stop()
                except Exception:
                    pass
                # Cleanup and exit process
                _cleanup_sdk()
                import os, sys
                try:
                    os._exit(0)
                except Exception:
                    try:
                        sys.exit(0)
                    except Exception:
                        pass

            try:
                menu = pystray.Menu(pystray.MenuItem("Abrir", _on_open), pystray.MenuItem("Sair", _on_quit))
                _tray_icon = pystray.Icon("wooting_rgb", img, "Wooting RGB", menu)

                def _run_icon():
                    try:
                        _tray_icon.run()
                    except Exception:
                        pass

                _tray_thread = threading.Thread(target=_run_icon, daemon=True)
                _tray_thread.start()
            except Exception:
                pass

        # Criar a tray (se possível) e cancelar o fecho da janela
        try:
            _create_tray()
            return False
        except Exception:
            # fallback: cleanup and allow close
            _cleanup_sdk()
            return True

    window.events.closing += on_closing

    webview.start(debug=("--debug" in sys.argv))

    # Cleanup extra após webview.start() retornar (janela já fechou)
    _cleanup_sdk()


if __name__ == "__main__":
    main()
