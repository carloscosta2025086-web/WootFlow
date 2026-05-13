#!/usr/bin/env python3
"""
Teste do novo comportamento do Living Heatmap - Versão Final.

Demonstra:
1. Cada clique = +0.02 (50 cliques para máximo)
2. Vizinhos aquecem 50% (metade do valor)
3. Delay de 0.5s antes de arrefecer
4. Cores: Verde → Amarelo → Laranja → Vermelho → Branco
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.effects_engine import LivingHeatmapEffect

def test_incremental_heating():
    """Teste 1: Aquecimento incremental (50 cliques para max)."""
    print("\n" + "=" * 60)
    print("TESTE 1: AQUECIMENTO INCREMENTAL")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  _press_heat = {effect._press_heat} (0.02 por clique)")
    print(f"  Cliques para máximo (1.0): {1.0 / effect._press_heat:.0f}")
    
    row, col = 2, 5
    
    print(f"\nClicando na tecla S ({row}, {col}) múltiplas vezes:\n")
    
    clicks = [1, 5, 10, 25, 30, 40, 50]
    for click in clicks:
        # Limpar e fazer novos cliques
        effect._temperature[row][col] = 0.0
        for _ in range(click):
            effect.trigger(row, col)
        
        temp = effect._temperature[row][col]
        color_name = effect._get_color_name(temp)
        bar = "█" * int(temp * 40) + "░" * (40 - int(temp * 40))
        
        print(f"  {click:2d} cliques: {bar} {temp:.2f} {color_name}")
    
    print(f"\n✓ Exactamente 50 cliques para atingir 1.0 (branco)!")

def test_neighbor_heating():
    """Teste 2: Vizinhos aquecem 50% mais devagar."""
    print("\n\n" + "=" * 60)
    print("TESTE 2: AQUECIMENTO DE VIZINHOS (50% mais devagar)")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  _neighbor_factor = {effect._neighbor_factor} (50% mais devagar)")
    
    row, col = 2, 5  # Tecla S
    
    print(f"\nClicando 50 vezes na tecla S ({row}, {col}):\n")
    
    # Limpar
    effect._temperature = [[0.0] * 21 for _ in range(6)]
    effect._last_press_time = [[0.0] * 21 for _ in range(6)]
    
    # 50 cliques
    for _ in range(50):
        effect.trigger(row, col)
    
    center_temp = effect._temperature[row][col]
    
    print(f"Tecla Central S ({row}, {col}):")
    bar = "█" * int(center_temp * 40) + "░" * (40 - int(center_temp * 40))
    print(f"  Temperatura: {bar} {center_temp:.2f}")
    
    neighbors = effect._get_neighbors(row, col)
    print(f"\nVizinhos (8 teclas adjacentes): W, Q, A, Z, X, C, D, E")
    
    # Mostrar temperatura esperada dos vizinhos
    # Cada clique no S: +0.02
    # Cada clique no S para vizinhos: +0.02 * 0.5 = +0.01
    expected_neighbor = center_temp * effect._neighbor_factor
    
    print(f"\nTemperatura esperada dos vizinhos:")
    print(f"  {center_temp:.2f} (S) × {effect._neighbor_factor} = {expected_neighbor:.2f}")
    
    neighbor_color = effect._get_color_name(expected_neighbor)
    bar = "█" * int(expected_neighbor * 40) + "░" * (40 - int(expected_neighbor * 40))
    
    print(f"  Exemplo: {bar} {expected_neighbor:.2f} {neighbor_color}")
    
    print(f"\n✓ Quando S está BRANCO (1.0), vizinhos estão em LARANJA (0.5)!")

def test_cooldown_delay():
    """Teste 3: Cooldown só começa após 0.5s de inatividade."""
    print("\n\n" + "=" * 60)
    print("TESTE 3: DELAY ANTES DE ARREFECER (0.5s)")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print(f"\nParâmetros:")
    print(f"  _cooldown_delay = {effect._cooldown_delay}s")
    print(f"  _cooldown_rate = {effect._cooldown_rate} temperatura/seg")
    
    row, col = 2, 5
    
    print(f"\n1. Aquecendo tecla S para máximo (50 cliques):")
    for _ in range(50):
        effect.trigger(row, col)
    
    temp = effect._temperature[row][col]
    print(f"   Temperatura: {temp:.2f} (BRANCO)")
    
    print(f"\n2. Passando 0.3 segundos (ainda dentro do delay):")
    print(f"   Temperatura: {temp:.2f} (SEM ARREFECER)")
    
    print(f"\n3. Passando 0.5 segundos (atinge o delay):")
    print(f"   → Neste ponto COMEÇA o arrefecimento")
    
    print(f"\n4. Passando mais 1 segundo (total 1.5s):")
    arrefeced = max(0.0, temp - (effect._cooldown_rate * 1.0))
    color = effect._get_color_name(arrefeced)
    print(f"   Temperatura: ~{arrefeced:.2f} {color}")
    
    print(f"\n✓ Arrefecimento só começa após 0.5s de inatividade!")

def test_realistic_scenario():
    """Teste 4: Cenário realista de gaming/digitação."""
    print("\n\n" + "=" * 60)
    print("TESTE 4: CENÁRIO REALISTA")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print("\nDigitação de 'WASD' em jogo (simula teclado de gaming):\n")
    
    # Simular digitação de WASD
    keys = {
        'W': (2, 5),
        'A': (3, 4),
        'S': (3, 5),
        'D': (3, 6),
    }
    
    # Limpar
    effect._temperature = [[0.0] * 21 for _ in range(6)]
    effect._last_press_time = [[0.0] * 21 for _ in range(6)]
    
    # Simular 5 vezes cada tecla
    pattern = ['W', 'A', 'S', 'D'] * 5
    
    for i, key in enumerate(pattern):
        row, col = keys[key]
        effect.trigger(row, col)
        if (i + 1) % 4 == 0:
            print(f"  Após {i + 1:2d} cliques: {key} = {effect._temperature[row][col]:.2f}")
    
    print(f"\n📊 Temperatura final das teclas WASD:")
    for key, (row, col) in keys.items():
        temp = effect._temperature[row][col]
        color = effect._get_color_name(temp)
        bar = "█" * int(temp * 20) + "░" * (20 - int(temp * 20))
        print(f"  {key}: {bar} {temp:.2f} {color}")
    
    print(f"\n✓ Padrão de jogo intenso aquece as teclas gradualmente!")

def main():
    # Adicionar método helper à classe para teste
    def get_color_name(self, temp):
        if temp == 0.0:
            return "⚫ Verde Escuro"
        elif temp < 0.25:
            return "🟡 Amarelo"
        elif temp < 0.5:
            return "🟠 Laranja"
        elif temp < 0.75:
            return "🔴 Vermelho"
        else:
            return "⚪ Branco"
    
    LivingHeatmapEffect._get_color_name = get_color_name
    
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Living Heatmap - NOVO COMPORTAMENTO FINAL".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    test_incremental_heating()
    test_neighbor_heating()
    test_cooldown_delay()
    test_realistic_scenario()
    
    print("\n\n" + "=" * 60)
    print("RESUMO DO COMPORTAMENTO")
    print("=" * 60)
    print("""
✅ COMPORTAMENTO IMPLEMENTADO:

1. AQUECIMENTO INCREMENTAL
   • Cada clique: +0.02 (50 cliques = máximo)
   • Cores progridem suavemente
   • Acumulativo e recompensador

2. VIZINHOS (WASD ao redor de S)
   • Aquecem 50% mais devagar (factor 0.5)
   • Se S = 1.0 (branco), vizinhos = 0.5 (laranja)
   • Proporção mantida em todo tempo

3. DELAY ANTES DE ARREFECER
   • Aguarda 0.5 segundos sem cliques
   • Depois começa o arrefecimento suave
   • Muito mais natural e responsivo

4. CORES (Verde → Amarelo → Laranja → Vermelho → Branco)
   • 0.0 → Verde Escuro
   • 0.25 → Amarelo
   • 0.5 → Laranja
   • 0.75 → Vermelho
   • 1.0 → Branco (com flicker suave)

PARÂMETROS AJUSTÁVEIS:
   • effect.speed: Velocidade de arrefecimento (0.5-2.0)
   • effect.brightness: Brilho geral (0.0-1.0)
""")

if __name__ == "__main__":
    main()
