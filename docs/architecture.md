# Arquitetura (fase de migracao)

## Estrutura alvo
- `main_desktop.py` e `server.py`: entrypoints e runtime
- `core/`: logica principal (efeitos, screen ambience, registry)
- `services/`: servicos auxiliares (perfis e persistencia)
- `utils/`: camada de hardware/SDK
- `tools/`: exemplos e utilitarios manuais
- `tests/`: testes automatizados

## Estado atual
- Runtime consolidado em `core/`, `services/` e `utils/`.
- Registry central de efeitos em `core/effect_registry.py`.

## Politica de migracao
1. Manter imports apenas para `core/`, `services/` e `utils/`.
2. Evitar wrappers na raiz.
3. Mover utilitarios apenas para `tools/`.
4. Remover codigo duplicado conforme checklist legacy.

## Regras
- Apenas um ponto de entrada para efeitos (registry).
- Estado/controlador de transicao centralizado.
- Ferramentas e exemplos fora do core.
