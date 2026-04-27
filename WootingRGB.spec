# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[('sdk', 'sdk'), ('config/config.json', '.'), ('config/rgb_settings.json', 'config'), ('ui/dist', 'ui/dist'), ('profiles', 'profiles')],
    hiddenimports=['uvicorn.logging', 'uvicorn.lifespan', 'uvicorn.lifespan.on', 'uvicorn.lifespan.off', 'uvicorn.protocols', 'uvicorn.protocols.http', 'uvicorn.protocols.http.auto', 'uvicorn.protocols.http.h11_impl', 'uvicorn.protocols.http.httptools_impl', 'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto', 'uvicorn.protocols.websockets.websockets_impl', 'uvicorn.loops', 'uvicorn.loops.auto', 'uvicorn.loops.asyncio', 'websockets', 'websockets.client', 'websockets.server', 'websockets.legacy', 'wsproto', 'webview', 'clr_loader', 'pythonnet', 'bottle', 'pyaudiowpatch', 'pystray', 'PIL', 'PIL.Image', 'PIL.ImageDraw', 'core.screen_ambience', 'core.screen_ambience_profile', 'mss', 'numpy'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    name='WootingRGB',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # <--- NÃO mostra janela preta/cmd
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    exclude_binaries=True,
    icon='assets/Wootflow_icon 256x256.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WootingRGB',
)
