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
