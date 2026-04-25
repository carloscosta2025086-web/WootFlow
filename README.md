# Wooting RGB

Aplicacao para controlar iluminacao RGB no teclado Wooting.

## Requisitos

- Python 3.10+
- Wooting conectado via USB
- Wootility fechada

## Executar

```bash
python main_desktop.py
```

## Funcionalidades

- Efeitos RGB
- Audio reativo
- Per-key
- Screen Ambience

## Configuracao

Arquivo: `config/config.json`

```json
{
  "check_interval": 5,
  "idle_effect": "breathing",
  "idle_color": [0, 200, 200]
}
```

## Build

```bash
cd ui
npm.cmd run build

cd ..
pyinstaller WootingRGB.spec --clean -y
```

## Binario (EXE)

- O `WootingRGB.exe` faz verificacao de pre-requisitos no arranque no Windows.
- Se faltar runtime essencial, tenta instalar automaticamente via `winget`:
  - Visual C++ Redistributable x64
  - Microsoft Edge WebView2 Runtime

## Releases

- O ficheiro `.github/workflows/release.yml` publica o binario automaticamente em **Releases** quando fizeres push de uma tag `v*`.
- O instalador de dependencias principal esta em `scripts/install_all.ps1`.
- `install_all.ps1` na raiz continua funcional como atalho de compatibilidade.
- Exemplo:

```bash
git tag v3.0.1
git push origin v3.0.1
```

- O workflow anexa ao release:
  - `WootingRGB.exe`
  - `WootingRGB-<tag>.zip`
