#!/usr/bin/env python3
"""
Exemplo de integração completa do efeito Living Heatmap.
Mostra como usar o efeito em contexto de aplicação real.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from core.effects_engine import LivingHeatmapEffect
from core.effect_registry import get_effect_class, EFFECT_LABELS


def example_basic_usage():
    """Exemplo 1: Uso básico do efeito."""
    print("=" * 60)
    print("EXEMPLO 1: Uso Básico")
    print("=" * 60)
    
    # Criar instância
    effect = LivingHeatmapEffect()
    
    # Simular algumas pressionamentos
    effect.trigger(2, 5)  # Row 2, Col 5 (próximo ao D)
    effect.trigger(2, 6)  # Row 2, Col 6 (próximo ao F)
    
    print("✓ Efeito criado e pressionamentos registados")
    print(f"  Nome: {effect.name}")
    print(f"  Brilho: {effect.brightness}")


def example_configuration():
    """Exemplo 2: Configuração personalizada."""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Configuração Personalizada")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    # Ajustar parâmetros
    effect.speed = 0.5                    # Arrefecimento mais lento
    effect.spread_strength = 0.6          # Propagação menos intensa
    effect.brightness = 0.8               # Brilho um pouco reduzido
    
    print("✓ Parâmetros ajustados:")
    print(f"  Speed: {effect.speed} (arrefecimento 50% mais lento)")
    print(f"  Spread: {effect.spread_strength} (propagação reduzida)")
    print(f"  Brightness: {effect.brightness}")


def example_from_registry():
    """Exemplo 3: Obter efeito do registry (como a app faria)."""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Acesso via Registry")
    print("=" * 60)
    
    # Assim a aplicação principal acede aos efeitos
    EffectClass = get_effect_class("living_heatmap")
    
    if EffectClass:
        effect = EffectClass()
        label = EFFECT_LABELS.get("living_heatmap")
        print(f"✓ Efeito obtido do registry:")
        print(f"  ID: living_heatmap")
        print(f"  Label: {label}")
        print(f"  Classe: {EffectClass.__name__}")
    else:
        print("✗ Efeito não encontrado!")


def example_keyboard_simulation():
    """Exemplo 4: Simulação de padrão de teclado."""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Simulação de Padrão de Escrita")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    # Simular digitação da palavra "HEATMAP"
    sequence = [
        (2, 8),   # H
        (2, 4),   # E
        (2, 1),   # A
        (1, 0),   # T
        (2, 1),   # A
        (3, 9),   # M
        (2, 1),   # A
        (3, 9),   # P
    ]
    
    print("Simulando digitação de 'HEATMAP':")
    for i, (row, col) in enumerate(sequence, 1):
        effect.trigger(row, col)
        print(f"  {i}. Pressionada tecla ({row}, {col})")
    
    print("\n✓ Padrão de heat trail criado!")
    print("  As teclas mostrarão cores progressivamente:")
    print("    - Teclas pressionadas: vermelho/branco")
    print("    - Vizinhos: laranja/amarelo")
    print("    - Distantes: verde")


def example_physics_parameters():
    """Exemplo 5: Entender a física do efeito."""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Física e Parâmetros Avançados")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print("Parâmetros de física internos:")
    print(f"  Cooldown Rate: {effect._cooldown_rate}")
    print(f"    → Quanto mais alto, mais rápido arrefece")
    print(f"    → Com speed=1.0, perde ~1.8 temperatura/seg")
    print()
    print(f"  Diffusion Factor: {effect._diffusion_factor}")
    print(f"    → Fração do calor que propaga para vizinhos")
    print(f"    → 0.25 = 25% por ciclo")
    print()
    print(f"  Press Heat: {effect._press_heat}")
    print(f"    → Temperatura inicial quando tecla é pressionada")
    print(f"    → 0.95 = quase máximo imediatamente")
    print()
    print(f"  Overheat Threshold: {effect.overheat_threshold}")
    print(f"    → A partir de {effect.overheat_threshold} ativa flickering")


def example_color_spectrum():
    """Exemplo 6: Visualizar o espectro de cores."""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Espectro de Cores da Temperatura")
    print("=" * 60)
    
    effect = LivingHeatmapEffect()
    
    print("Progressão de cores (temperatura 0 → 1):\n")
    
    temps = [
        (0.0, "Inativo"),
        (0.1, "Verde escuro"),
        (0.25, "Verde claro"),
        (0.4, "Amarelo"),
        (0.6, "Laranja"),
        (0.75, "Vermelho"),
        (0.92, "Vermelho brilhante"),
        (1.0, "Branco (overheat)"),
    ]
    
    for temp, desc in temps:
        r, g, b = effect._temperature_to_color(temp)
        # Criar uma visualização ASCII simples
        bar = "█" * int(temp * 20)
        print(f"  {temp:.2f} {bar:20} RGB({r:3d}, {g:3d}, {b:3d}) - {desc}")


def main():
    """Executa todos os exemplos."""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  Living Heatmap Effect - Exemplos de Integração".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    
    example_basic_usage()
    example_configuration()
    example_from_registry()
    example_keyboard_simulation()
    example_physics_parameters()
    example_color_spectrum()
    
    print("\n" + "=" * 60)
    print("TODOS OS EXEMPLOS COMPLETADOS COM SUCESSO!")
    print("=" * 60)
    print("\n💡 Próximos passos:")
    print("  1. Integrar no menu de efeitos da UI")
    print("  2. Adicionar controles para ajustar speed/spread/brightness")
    print("  3. Testar com teclado real Wooting")
    print("  4. Customizar cores conforme preferência")
    print()


if __name__ == "__main__":
    main()
