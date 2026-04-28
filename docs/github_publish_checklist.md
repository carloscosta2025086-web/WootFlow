# GitHub Publish Checklist (WootFlow)

## Objetivo
Este repositorio deve guardar codigo fonte, configuracao, documentacao e automacao.
Artefactos de build e ficheiros de maquina local devem ficar fora do Git.

## Deve ir para o GitHub
- Codigo fonte Python e UI.
- Configuracoes versionadas (sem segredos).
- Scripts de build e instalador.
- Workflows CI/CD.
- Testes automaticos.
- Documentacao tecnica e de release.
- Assets estaticos necessarios ao runtime (icones, perfis, SDK runtime necessario).

## Nao deve ir para o GitHub
- Dist/build locais: build/, dist/, installer/output/.
- Caches e temporarios: __pycache__/, .pytest_cache/, .ruff_cache/, .mypy_cache/, .artifacts/.
- Ambientes locais: .venv/, node_modules/.
- Logs e dumps: *.log.
- Binarios gerados localmente para debug sem necessidade de runtime.
- Segredos: tokens, chaves, passwords, ficheiros .env com credenciais.

## Regras praticas para este projeto
1. O output final portable deve existir apenas em dist/WootFlow/ durante build local.
2. O instalador final deve ir para installer/output/ e ser publicado em GitHub Releases, nao comitado.
3. Ficheiros de prerequisitos em installer/prereqs/ devem ser baixados via script e nao comitados (manter apenas .gitkeep).
4. Artefactos intermédios do PyInstaller devem ir para .artifacts/pyinstaller/work.

## Checklist antes de publicar
1. Confirmar branch limpa:
   - git status
2. Confirmar que nao ha artefactos rastreados indevidos:
   - git ls-files | findstr /R "^build/ ^dist/ ^installer/output/ ^.venv/"
3. Correr CI local minima:
   - python -m pytest tests -q
4. Validar build release:
   - powershell -ExecutionPolicy Bypass -File .\\scripts\\build_installer.ps1 -Version X.Y.Z
5. Validar output:
   - dist/WootFlow/WootFlow.exe
   - installer/output/WootFlow-Setup-X.Y.Z.exe

## Melhores praticas recomendadas (faltam no repo)
- LICENSE
- CONTRIBUTING.md
- SECURITY.md
- CHANGELOG.md
- .github/ISSUE_TEMPLATE/
- .github/pull_request_template.md

## Nota sobre artefactos atualmente rastreados
- Rever necessidade de ui/tsconfig.tsbuildinfo estar no Git (normalmente nao deve estar).
- Rever necessidade de sdk/wooting-rgb-sdk64.pdb no Git (normalmente pode sair se nao for necessario para runtime).
