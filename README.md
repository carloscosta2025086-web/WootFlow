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
- O `WootingRGB.exe` tambem verifica atualizacoes automaticamente (GitHub Releases).
  - Se houver nova versao, avisa o utilizador.
  - Se o utilizador aceitar, faz download do novo `WootingRGB.exe` e aplica update automaticamente.

## Releases

- O ficheiro `.github/workflows/release.yml` publica o binario automaticamente em **Releases** quando fizeres push de uma tag `v*`.
- O instalador de dependencias principal esta em `scripts/install_all.ps1`.
- `install_all.ps1` na raiz continua funcional como atalho de compatibilidade.
- O workflow publica tambem um instalador Windows `WootFlow-Setup-<versao>.exe`.
- Exemplo:

```bash
git tag v3.0.1
git push origin v3.0.1
```

- O workflow anexa ao release:
  - `WootingRGB.exe`
  - `WootingRGB-<tag>.zip`
  - `WootFlow-Setup-<versao>.exe`

## Instalador Windows

Solucao recomendada:

- `PyInstaller` gera a aplicacao Windows.
- `Inno Setup` gera um unico `Setup.exe` para o utilizador final.
- O instalador copia a app para `Program Files\WootFlow`, cria atalhos, instala/desinstala limpo e evita reinstalar pre-requisitos que ja existem.

Estrutura:

- `installer/WootFlowInstaller.iss`: script do Inno Setup.
- `installer/prereqs/`: prerequisitos Windows incluidos no setup.
- `installer/output/`: instaladores gerados.
- `scripts/download_installer_prereqs.ps1`: transfere prerequisitos do instalador.
- `scripts/build_installer.ps1`: build automatizado do `Setup.exe`.

Comportamento do Setup.exe:

- Instala a app em `Program Files\WootFlow`.
- Cria atalho no menu iniciar e opcionalmente no desktop.
- Verifica e instala apenas se necessario:
  - Visual C++ Redistributable x64
  - WebView2 Runtime
- Mostra progresso e logs do proprio instalador (`SetupLogging=yes`).
- Depois da instalacao, a app funciona sem precisar de Python, Node.js ou npm no PC do utilizador.

Build local do instalador:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\download_installer_prereqs.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\build_installer.ps1 -Version 3.0.6
```

Notas:

- O script transfere sempre o `vc_redist.x64.exe` oficial.
- Para WebView2, o script transfere por omissao o bootstrapper pequeno. Isso da instalacao automatica em um clique, mas pode usar internet durante o setup.
- Se quiseres media 100% offline, coloca manualmente `MicrosoftEdgeWebView2RuntimeInstallerX64.exe` em `installer/prereqs/` antes de correr `build_installer.ps1`.

Boas praticas para GitHub Releases:

- Publicar sempre os 3 artefactos:
  - binario portatil (`WootingRGB.exe`)
  - zip (`WootingRGB-<tag>.zip`)
  - instalador (`WootFlow-Setup-<versao>.exe`)
- Para utilizador final, divulgar o `WootFlow-Setup-<versao>.exe` como download principal.
- Manter `installer/prereqs/*.exe` e `installer/output/*` fora do Git; os artefactos finais devem ir apenas para Releases.
