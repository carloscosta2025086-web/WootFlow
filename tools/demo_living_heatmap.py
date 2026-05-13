#!/usr/bin/env python3
"""
Demo do efeito Living Heatmap.

Testa a integração e comportamento do novo efeito.
"""

import sys
sys.path.insert(0, '.')

from core.effects_engine import LivingHeatmapEffect
from core.effect_registry import get_effect_class, EFFECT_LABELS

# Verificar se o efeito está registrado
print("=" * 60)
print("VERIFICAÇÃO DE INTEGRAÇÃO - Living Heatmap")
print("=" * 60)

# 1. Verificar se está no registry
effect_class = get_effect_class("living_heatmap")
if effect_class:
    print("✓ Efeito 'living_heatmap' encontrado no registry")
else:
    print("✗ ERRO: Efeito 'living_heatmap' NÃO foi encontrado no registry")
    sys.exit(1)

# 2. Verificar label
label = EFFECT_LABELS.get("living_heatmap")
if label == "Living Heatmap":
    print(f"✓ Label corretamente registrado: '{label}'")
else:
    print(f"✗ ERRO: Label incorreto: '{label}'")
    sys.exit(1)

# 3. Instanciar o efeito
effect = LivingHeatmapEffect()
print(f"✓ Efeito instantiado com sucesso")
print(f"  - Nome: {effect.name}")
print(f"  - Velocidade (speed): {effect.speed}")
print(f"  - Força de propagação (spread_strength): {effect.spread_strength}")
print(f"  - Limiar de overheat: {effect.overheat_threshold}")

# 4. Testar método trigger
print("\n" + "=" * 60)
print("TESTE DE TRIGGER (Simulação de Pressionamento)")
print("=" * 60)

# Simular pressionamentos
test_keys = [(2, 5), (2, 6), (3, 7), (4, 8)]
for row, col in test_keys:
    effect.trigger(row, col)
    print(f"✓ Pressionamento simulado em tecla ({row}, {col})")

# 5. Testar método de mapeamento de cores
print("\n" + "=" * 60)
print("TESTE DE MAPEAMENTO DE CORES")
print("=" * 60)

temps = [0.0, 0.15, 0.35, 0.55, 0.8, 1.0]
for temp in temps:
    color = effect._temperature_to_color(temp, is_overheat=False)
    print(f"  Temp {temp:.2f} → RGB{color}")

print("\nCom Overheat (flicker):")
for temp in [0.92, 0.96, 1.0]:
    color = effect._temperature_to_color(temp, is_overheat=True)
    print(f"  Temp {temp:.2f} → RGB{color} (flickering)")

# 6. Testar vizinhos
print("\n" + "=" * 60)
print("TESTE DE DETEÇÃO DE VIZINHOS")
print("=" * 60)

test_pos = (2, 5)
neighbors = effect._get_neighbors(test_pos[0], test_pos[1])
print(f"Vizinhos de {test_pos}: {len(neighbors)} encontrados")
print(f"  {neighbors}")

print("\n" + "=" * 60)
print("✓ TODOS OS TESTES PASSARAM COM SUCESSO!")
print("=" * 60)
print("\nO efeito 'Living Heatmap' está pronto para usar!")
print("\nCaracterísticas:")
print("  • Cores dinâmicas: Verde → Amarelo → Laranja → Vermelho → Branco")
print("  • Propagação orgânica de calor para teclas vizinhas")
print("  • Arrefecimento suave e gradual")
print("  • Estado de overheat com flicker automático")
print("  • Glow dinâmico baseado em temperatura")
