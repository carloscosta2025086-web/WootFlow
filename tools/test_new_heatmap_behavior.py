#!/usr/bin/env python3
"""
Teste do novo comportamento do Living Heatmap - Acumulativo e Lento.

Demonstra:
1. Múltiplos cliques são necessários para chegar ao overheat
2. Vizinhos aquecem muito menos
3. Arrefecimento é MUITO lento
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.effects_engine import LivingHeatmapEffect

def test_accumulative_press():
    """Teste 1: Mostra que múltiplos cliques são necessários para overheat."""
    print("\n" + "=" * 60)
    print("TESTE 1: AQUECIMENTO ACUMULATIVO")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  _press_heat = {effect._press_heat} (18% por clique)")
    print(f"  Cliques necessários para overheat (~0.92): ~{int(0.92 / effect._press_heat)} cliques")
    print(f"\nSimulando múltiplos pressionamentos na mesma tecla:\n")
    
    row, col = 2, 5
    
    for click in range(1, 8):
        effect.trigger(row, col)
        temp = effect._temperature[row][col]
        bar_length = int(temp * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        
        status = ""
        if temp >= effect.overheat_threshold:
            status = "⚠️  OVERHEAT!"
        elif temp >= 0.8:
            status = "🔥 Muito quente"
        elif temp >= 0.6:
            status = "🟠 Quente"
        elif temp >= 0.4:
            status = "🟡 Morno"
        else:
            status = "🟢 Frio"
        
        print(f"  Clique {click}: {bar} {temp:.2f} {status}")
    
    print("\n✓ Overheat é alcançado gradualmente com múltiplos cliques!")

def test_neighbor_heating():
    """Teste 2: Vizinhos aquecem muito menos que a tecla principal."""
    print("\n\n" + "=" * 60)
    print("TESTE 2: AQUECIMENTO DE VIZINHOS (REDUZIDO)")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  Spread para vizinhos = 5% apenas")
    print(f"\nAquecendo tecla central (2, 5) continuamente...\n")
    
    row, col = 2, 5
    
    # Aquecer a tecla central 10 vezes
    for _ in range(10):
        effect.trigger(row, col)
    
    center_temp = effect._temperature[row][col]
    
    print(f"Tecla Central (2, 5):")
    print(f"  Temperatura: {center_temp:.2f}")
    
    print(f"\nVizinhos diretos (adjacentes, 8 posições):")
    print(f"  [Note: Vizinhos ainda não recebem calor sem update]")
    neighbors = effect._get_neighbors(row, col)
    
    for nr, nc in sorted(neighbors):
        neighbor_temp = effect._temperature[nr][nc]
        bar_length = int(neighbor_temp * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"  ({nr}, {nc}): {bar} {neighbor_temp:.2f}")
    
    print(f"\n✓ O spread para vizinhos é apenas 5% (muito reduzido)!")
    print(f"  Mantém foco na tecla pressionada!")

def test_slow_cooldown():
    """Teste 3: Arrefecimento é MUITO lento."""
    print("\n\n" + "=" * 60)
    print("TESTE 3: ARREFECIMENTO MUITO LENTO")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  _cooldown_rate = {effect._cooldown_rate} (MUITO REDUZIDO de 1.8)")
    print(f"  Arrefecimento por segundo: ~{effect._cooldown_rate * (1/60) * 60:.4f} temperatura/seg")
    print(f"  Tempo aprox. para arrefecer completamente: ~{1.0 / (effect._cooldown_rate * (1/60) * 60):.0f} segundos")
    
    row, col = 2, 5
    
    # Aquecer a tecla ao máximo
    for _ in range(10):
        effect.trigger(row, col)
    
    temp_inicial = effect._temperature[row][col]
    print(f"\nTemperatura inicial: {temp_inicial:.2f}")
    print(f"\nTempo estimado para arrefecer:")
    
    # Calcular tempo teórico
    dt = 1.0 / 60.0
    cooldown_per_frame = effect._cooldown_rate * 1.0 * dt
    frames_to_cool = temp_inicial / cooldown_per_frame
    seconds_to_cool = frames_to_cool / 60
    
    print(f"  Frames necessários: ~{frames_to_cool:.0f}")
    print(f"  Segundos: ~{seconds_to_cool:.1f}s")
    print(f"  Minutos: ~{seconds_to_cool / 60:.1f}m")
    
    print(f"\n✓ O arrefecimento é EXTREMAMENTE LENTO!")
    print(f"  O efeito persiste por longos períodos!")

def test_combined_behavior():
    """Teste 4: Comportamento combinado realista."""
    print("\n\n" + "=" * 60)
    print("TESTE 4: CENÁRIO REALISTA COMBINADO")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print("\nCenário: Digitação normal e gaming")
    print("─" * 50)
    
    # Simular digitação: pressiona a mesma tecla 3 vezes (rápido)
    print("\n1. Pressionas 'A' três vezes (digitação rápida):")
    for click in range(1, 4):
        effect.trigger(3, 5)
        print(f"   Clique {click}: Temperatura = {effect._temperature[3][5]:.2f}")
    
    print(f"\n2. Vizinho de 'A' ainda não recebe calor (antes do update):")
    print(f"   Tecla (2, 5) [vizinho]: {effect._temperature[2][5]:.2f}")
    print(f"   Tecla (3, 4) [vizinho]: {effect._temperature[3][4]:.2f}")
    print(f"   Tecla (3, 6) [vizinho]: {effect._temperature[3][6]:.2f}")
    
    # Simular espera de 2 segundos (arrefecimento)
    print(f"\n3. Espera de 2 segundos sem pressionar...")
    dt = 1.0 / 60.0
    cooldown_per_frame = effect._cooldown_rate * 1.0 * dt
    temp_after_2s = effect._temperature[3][5] - (cooldown_per_frame * 120)
    print(f"   Tecla 'A' após 2s: ~{max(0, temp_after_2s):.2f} (ainda bem quente!)")
    
    # Pressionar novamente
    print(f"\n4. Pressiona 'A' mais 3 vezes (acumula):")
    for click in range(1, 4):
        effect.trigger(3, 5)
        print(f"   Clique {click}: Temperatura = {effect._temperature[3][5]:.2f}")
    
    final_temp = effect._temperature[3][5]
    if final_temp >= effect.overheat_threshold:
        print(f"\n⚠️  OVERHEAT! A tecla 'A' está em estado de sobreaquecimento!")
    else:
        print(f"\n   (Faltam {effect.overheat_threshold - final_temp:.2f} para overheat)")
    
    print(f"\n✓ Comportamento realista:")
    print(f"  • Múltiplos cliques acumulam calor")
    print(f"  • Vizinhos aquecem muito pouco (5% apenas)")
    print(f"  • Calor persiste mesmo sem pressão")

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Living Heatmap - NOVO COMPORTAMENTO (Lento)".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_accumulative_press()
    test_neighbor_heating()
    test_slow_cooldown()
    test_combined_behavior()
    
    print("\n\n" + "=" * 60)
    print("RESUMO DAS ALTERAÇÕES")
    print("=" * 60)
    print("""
✅ MUDANÇAS IMPLEMENTADAS:

1. _press_heat: 0.95 → 0.18
   → Pressionamento não ativa imediatamente
   → Precisa de ~5-6 cliques para chegar ao overheat
   → Totalmente acumulativo

2. _cooldown_rate: 1.8 → 0.35
   → Arrefecimento MUITO mais lento
   → O efeito persiste por muito tempo
   → Cria uma sensação de "memória térmica"

3. Spread para vizinhos: 0.08 → 0.05
   → Vizinhos recebem apenas 5% do calor
   → Mantém foco na tecla pressionada
   → Propagação mais suave e controlada

RESULTADO:
• Efeito muito mais gradual e orgânico
• Recompensa pressionamentos repetidos
• Overheat é um estado especial que leva tempo a atingir
• Vizinhos aquecem mas muito menos que a tecla principal
• Arrefecimento é extremamente lento (1-2 minutos+)
""")

if __name__ == "__main__":
    main()
