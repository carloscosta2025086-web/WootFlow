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

# Garantir que imports relativos funcionam no PyInstaller
if getattr(sys, "frozen", False):
    _BASE = os.path.dirname(sys.executable)
else:
    _BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASE)

# Log de diagnóstico — escreve ao lado do exe ou do script
_LOG_PATH = os.path.join(_BASE, "wootflow_debug.log")
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
        uvicorn.run(_srv.app, host="127.0.0.1", port=9120, log_level="warning")
        _log.info("uvicorn exited cleanly")
    except Exception as _exc:
        _log.exception("SERVER CRASHED: %s", _exc)


def _wait_for_server(timeout: float = 10.0):
    """Espera até o server responder."""
    import urllib.request
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            urllib.request.urlopen("http://127.0.0.1:9120/ws", timeout=1)
        except Exception:
            # Any response (even 4xx) means server is up
            # Only ConnectionRefused means not ready yet
            try:
                import urllib.error
                urllib.request.urlopen("http://127.0.0.1:9120/", timeout=1)
                return True
            except urllib.error.URLError:
                time.sleep(0.2)
                continue
            except Exception:
                return True
    return False


def _cleanup_sdk():
    """Força cleanup do SDK ao fechar a janela/processo."""
    try:
        _srv._force_cleanup()
    except Exception:
        pass


def main():
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

    # Wait for server to be ready
    _wait_for_server()

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
