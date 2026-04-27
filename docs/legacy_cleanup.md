# Legacy Cleanup Checklist (Fase 3)

## Estado atual
Wrappers legacy de raiz foram removidos.

## Verificacoes executadas
1. Imports migrados para modulos canónicos (`core`, `services`, `utils`).
2. Ferramentas em `tools/` atualizadas para imports diretos.
3. CI e testes básicos continuam válidos.

## Proximos pontos de limpeza
1. Revisar periodicamente artefactos gerados (`build`, `dist`, caches) e manter fora do Git.
2. Manter o registry único de efeitos em `core/effect_registry.py`.
3. Evitar novos wrappers de compatibilidade na raiz.
