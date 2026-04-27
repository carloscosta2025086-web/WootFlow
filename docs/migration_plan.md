# Plano de migracao

## Fase 1
- Workflow dev sem EXE
- Testes basicos e lint em CI
- Documentacao minima

## Fase 2
- Estrutura consolidada em `core/`, `services/` e `utils/`
- Registry unico de efeitos (`core/effect_registry.py`)
- Separacao entre runtime e ferramentas (`tools/`)

## Fase 3
- Remocao de wrappers legacy
- Simplificacao de codigo duplicado
- CI mais estrito (escopo de lint ampliado)
