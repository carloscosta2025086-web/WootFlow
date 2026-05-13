#!/usr/bin/env python3
"""
Visualização ASCII do efeito Living Heatmap em ação.
Ajuda a entender o comportamento e a propagação de calor.
"""

# Mapa de caracteres para representar temperatura
TEMP_CHARS = {
    0.0: '░',  # Muito frio
    0.1: '░',
    0.2: '▒',  # Frio
    0.3: '▒',
    0.4: '▓',  # Morno
    0.5: '▓',
    0.6: '█',  # Quente
    0.7: '█',
    0.8: '█',  # Muito quente
    0.9: '◆',  # Overheat
    1.0: '●',  # Máximo overheat
}

def get_char_for_temp(temp):
    """Retorna um caractere ASCII baseado em temperatura."""
    if temp >= 0.9:
        return '●'
    elif temp >= 0.8:
        return '█'
    elif temp >= 0.6:
        return '▓'
    elif temp >= 0.4:
        return '▒'
    elif temp >= 0.1:
        return '░'
    else:
        return ' '

def visualize_heatmap(temperatures, title=""):
    """Visualiza uma matrix de temperaturas."""
    if title:
        print(f"\n{title}")
    print("┌" + "─" * 40 + "┐")
    for row in temperatures:
        print("│", end="")
        for temp in row:
            print(get_char_for_temp(temp), end="")
        print(" │")
    print("└" + "─" * 40 + "┘")

def demo_single_press():
    """Demonstra o efeito de um único pressionamento."""
    print("\n" + "=" * 50)
    print("CENÁRIO 1: PRESSIONAMENTO ÚNICO")
    print("=" * 50)
    
    temps = [[0.0 for _ in range(5)] for _ in range(5)]
    
    print("\n1. Tecla central pressionada (T=0)")
    temps[2][2] = 0.95
    visualize_heatmap(temps, "Frame 0 (pressionado):")
    
    print("\n2. Propagação começando (T=1)")
    temps[2][2] = 0.85  # Arrefece um pouco
    for i in range(1, 4):
        for j in range(1, 4):
            if not (i == 2 and j == 2):
                dist = max(abs(i-2), abs(j-2))
                temps[i][j] = max(temps[i][j], 0.95 * (1 - dist * 0.3))
    visualize_heatmap(temps, "Frame 1 (propagação inicial):")
    
    print("\n3. Espalhamento máximo (T=2)")
    # Aplicar mais uma rodada de cooling
    for i in range(5):
        for j in range(5):
            temps[i][j] *= 0.7
    visualize_heatmap(temps, "Frame 2 (espalhado):")
    
    print("\n4. Arrefecimento (T=3)")
    for i in range(5):
        for j in range(5):
            temps[i][j] *= 0.6
    visualize_heatmap(temps, "Frame 3 (arrefecendo):")
    
    print("\n✓ A tecla volta ao estado verde escuro gradualmente")

def demo_wave_typing():
    """Demonstra digitação em padrão."""
    print("\n\n" + "=" * 50)
    print("CENÁRIO 2: DIGITAÇÃO RÁPIDA (WAVE)")
    print("=" * 50)
    
    temps = [[0.0 for _ in range(8)] for _ in range(3)]
    
    # Simular digitação: esquerda → direita
    sequence = [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    
    for idx, (row, col) in enumerate(sequence):
        print(f"\nDigitação {idx + 1}: Tecla ({row}, {col})")
        
        # Aplicar cooldown
        for i in range(3):
            for j in range(8):
                temps[i][j] *= 0.8
        
        # Pressionamento novo
        temps[row][col] = 0.95
        
        # Propagação rápida para vizinhos
        for i in range(3):
            for j in range(8):
                if (i, j) != (row, col):
                    dist = abs(i - row) + abs(j - col)
                    if dist <= 2:
                        temps[i][j] = max(temps[i][j], 0.95 * (1 - dist * 0.25))
        
        visualize_heatmap(temps, f"Frame {idx}:")
        
        if idx == len(sequence) - 1:
            print("✓ Heat trail segue o padrão de digitação")

def demo_sustained_press():
    """Demonstra pressionamento sustentado (gaming)."""
    print("\n\n" + "=" * 50)
    print("CENÁRIO 3: PRESSIONAMENTO SUSTENTADO (WASD)")
    print("=" * 50)
    
    temps = [[0.0 for _ in range(5)] for _ in range(5)]
    
    # W, A, S, D posições aproximadas
    wasd = [(1, 2), (2, 1), (2, 2), (2, 3)]
    
    print("\n1. Primeiras pressionagens")
    for pos in wasd:
        temps[pos[0]][pos[1]] = 0.95
    visualize_heatmap(temps, "Frame 1 (WASD aquecido):")
    
    print("\n2. Pressão contínua (acumulação)")
    for pos in wasd:
        temps[pos[0]][pos[1]] = min(1.0, temps[pos[0]][pos[1]] + 0.3)
    visualize_heatmap(temps, "Frame 5 (acumulação):")
    
    print("\n3. Overheat! (máximo brilho)")
    for pos in wasd:
        temps[pos[0]][pos[1]] = 1.0
    visualize_heatmap(temps, "Frame 10 (OVERHEAT - flickering ●):")
    
    print("\n4. Libertação (arrefecimento rápido)")
    # Para de pressionar
    for i in range(5):
        for j in range(5):
            temps[i][j] *= 0.85
    visualize_heatmap(temps, "Frame 15 (após soltar):")
    
    print("\n✓ Volta ao normal após ~1-2 segundos")

def demo_legend():
    """Mostra a legenda de caracteres."""
    print("\n\n" + "=" * 50)
    print("LEGENDA DE CORES")
    print("=" * 50)
    
    legend = [
        ("   ", "Completamente frio (0%)"),
        ("░░░", "Frio (10-20%)"),
        ("▒▒▒", "Morno (40-50%)"),
        ("▓▓▓", "Quente (60-80%)"),
        ("███", "Muito quente (80%+)"),
        ("●●●", "Overheat/Máximo (100%+) com flicker"),
    ]
    
    for char, desc in legend:
        print(f"  {char}  →  {desc}")

def main():
    print("\n")
    print("╔" + "=" * 48 + "╗")
    print("║" + " " * 48 + "║")
    print("║" + "  Living Heatmap - Visualização ASCII".center(48) + "║")
    print("║" + " " * 48 + "║")
    print("╚" + "=" * 48 + "╝")
    
    demo_legend()
    demo_single_press()
    demo_wave_typing()
    demo_sustained_press()
    
    print("\n\n" + "=" * 50)
    print("RESUMO DO COMPORTAMENTO")
    print("=" * 50)
    print("""
1. CORES:
   • Verde escuro → Amarelo → Laranja → Vermelho → Branco
   • Transição suave em tempo real

2. PROPAGAÇÃO:
   • Calor espalha para 8 vizinhos simultaneamente
   • Gradiente natural de quente → frio

3. ARREFECIMENTO:
   • Todas as teclas perdem temperatura ao longo do tempo
   • Velocidade ajustável via 'speed' (0.5x → 2.0x)

4. OVERHEAT:
   • A 92%+ de temperatura ativa flickering
   • Centro branco com oscilação 12Hz
   • Cria sensação realista de sobreaquecimento

5. GLOW:
   • Brilho varia de 40% (frio) a 100% (quente)
   • Realça teclas ativas e propagação

O efeito é totalmente fluido, responsivo e fisicamente plausível! ✨
""")

if __name__ == "__main__":
    main()
