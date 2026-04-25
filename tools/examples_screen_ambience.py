"""
Exemplos de uso e testes para Screen Ambience
Demonstra os diferentes modos e configurações disponíveis
"""

import time
from wooting_rgb import WootingRGB
from screen_ambience_profile import load_ambience_profile


def example_1_basic_usage():
    """Exemplo 1: Uso básico - Ativar e usar Screen Ambience."""
    print("\n" + "=" * 60)
    print("EXEMPLO 1: Uso Básico")
    print("=" * 60)
    
    # Conectar
    print("\n1. Conectando ao teclado...")
    kb = WootingRGB()
    print("   ✓ Teclado conectado")
    
    # Carregar perfil
    print("\n2. Carregando Screen Ambience...")
    profile = load_ambience_profile(kb)
    print("   ✓ Perfil carregado")
    
    # Ativar
    print("\n3. Ativando Screen Ambience...")
    profile.activate()
    print("   ✓ Screen Ambience ativo!")
    
    # Deixar executar
    print("\n4. Executando por 10 segundos...")
    print("   Observe as cores do ecrã serem replicadas no teclado")
    time.sleep(10)
    
    # Desativar
    print("\n5. Desativando...")
    profile.deactivate()
    print("   ✓ Concluído")


def example_2_mode_switching():
    """Exemplo 2: Mudar entre diferentes modos."""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Switching de Modos")
    print("=" * 60)
    
    kb = WootingRGB()
    profile = load_ambience_profile(kb)
    
    modes = ["cinematic", "dynamic", "gaming"]
    
    for mode in modes:
        print(f"\n🎬 Testando modo: {mode.upper()}")
        profile.set_mode(mode)
        profile.activate()
        
        stats = profile.get_stats()
        print(f"   FPS configurado: {stats.get('mode', 'N/A')}")
        
        print(f"   Executando por 5 segundos...")
        time.sleep(5)
        
        stats = profile.get_stats()
        print(f"   FPS real: {stats.get('actual_fps', 0):.1f}")
        print(f"   Frame time: {stats.get('avg_frame_time_ms', 0):.2f}ms")
        
        profile.deactivate()
    
    print("\n✓ Teste de modos concluído")


def example_3_brightness_control():
    """Exemplo 3: Controlar brilho dinamicamente."""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Controle de Brilho")
    print("=" * 60)
    
    kb = WootingRGB()
    profile = load_ambience_profile(kb)
    profile.activate()
    
    print("\nAjustando brilho de 0.3 até 2.0...")
    
    for brightness in [0.3, 0.5, 0.7, 1.0, 1.3, 1.6, 2.0]:
        print(f"\n  Brilho: {brightness:.1f}")
        profile.set_brightness(brightness)
        time.sleep(2)
    
    profile.deactivate()
    print("\n✓ Teste de brilho concluído")


def example_4_long_running():
    """Exemplo 4: Execução contínua com monitoramento."""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Monitoramento de Performance")
    print("=" * 60)
    
    kb = WootingRGB()
    profile = load_ambience_profile(kb)
    
    print("\nMode: Dynamic (30 segundos de monitoramento)")
    profile.set_mode("dynamic")
    profile.activate()
    
    print("\nTempo (s) | FPS Real | Frame Time (ms) | Grid")
    print("-" * 50)
    
    for i in range(30):
        stats = profile.get_stats()
        elapsed = i + 1
        fps = stats.get('actual_fps', 0)
        frame_time = stats.get('avg_frame_time_ms', 0)
        grid = stats.get('grid_size', 0)
        
        print(f"  {elapsed:2d}     | {fps:6.1f} | {frame_time:14.2f} | {grid}x{grid}")
        
        time.sleep(1)
    
    profile.deactivate()
    print("\n✓ Monitoramento concluído")


def example_5_custom_config():
    """Exemplo 5: Usar configuração customizada."""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Configuração Customizada")
    print("=" * 60)
    
    from screen_ambience import ScreenAmbienceConfig, ScreenAmbienceEngine
    
    # Criar config customizada
    config = ScreenAmbienceConfig(
        mode="custom",
        fps=45,  # Entre cinematic (30) e dynamic (60)
        grid_size=4,  # Grid 4x4
        brightness=1.15,
        color_sensitivity="high",
        smoothing_factor=0.65,
        exclude_black=True,
        black_threshold=25,
    )
    
    print("\nConfigurações customizadas:")
    print(f"  FPS: {config.fps}")
    print(f"  Grid: {config.grid_size}x{config.grid_size}")
    print(f"  Brilho: {config.brightness}")
    print(f"  Sensibilidade de cor: {config.color_sensitivity}")
    print(f"  Suavização: {config.smoothing_factor}")
    
    # Criar engine
    engine = ScreenAmbienceEngine(config)
    
    print("\n  Iniciando engine...")
    engine.start()
    
    print("  Executando por 10 segundos...")
    time.sleep(10)
    
    # Stats
    stats = engine.get_stats()
    print(f"\n  FPS real: {stats.get('actual_fps', 0):.1f}")
    print(f"  Frame time: {stats.get('avg_frame_time_ms', 0):.2f}ms")
    
    engine.stop()
    print("\n✓ Teste de configuração customizada concluído")


def example_6_interactive():
    """Exemplo 6: Interface interativa simples."""
    print("\n" + "=" * 60)
    print("EXEMPLO 6: Interface Interativa")
    print("=" * 60)
    
    kb = WootingRGB()
    profile = load_ambience_profile(kb)
    
    print("\nMenu interativo:")
    print("  A - Ativar Screen Ambience")
    print("  D - Desativar")
    print("  M - Mudar modo")
    print("  B - Ajustar brilho")
    print("  S - Ver status")
    print("  Q - Sair")
    
    while True:
        choice = input("\nEscolha (A/D/M/B/S/Q): ").upper()
        
        if choice == 'A':
            profile.activate()
            print("✓ Ativado")
        
        elif choice == 'D':
            profile.deactivate()
            print("✓ Desativado")
        
        elif choice == 'M':
            mode = input("Modo (cinematic/dynamic/gaming): ").lower()
            if mode in ["cinematic", "dynamic", "gaming"]:
                profile.set_mode(mode)
                print(f"✓ Modo: {mode}")
            else:
                print("✗ Modo inválido")
        
        elif choice == 'B':
            try:
                bright = float(input("Brilho (0.0-2.0): "))
                profile.set_brightness(bright)
                print(f"✓ Brilho: {bright}")
            except ValueError:
                print("✗ Valor inválido")
        
        elif choice == 'S':
            profile.print_status()
        
        elif choice == 'Q':
            profile.deactivate()
            print("Sair...")
            break
        
        else:
            print("✗ Opção inválida")


def main():
    """Executa todos os exemplos."""
    print("\n" + "=" * 60)
    print("🎨 Screen Ambience - Exemplos de Uso")
    print("=" * 60)
    
    examples = [
        ("Uso Básico", example_1_basic_usage),
        ("Mode Switching", example_2_mode_switching),
        ("Controle de Brilho", example_3_brightness_control),
        ("Monitoramento de Performance", example_4_long_running),
        ("Configuração Customizada", example_5_custom_config),
        ("Interface Interativa", example_6_interactive),
    ]
    
    print("\nExemplos disponíveis:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i} - {name}")
    print("  0 - Executar todos")
    print("  Q - Sair")
    
    while True:
        choice = input("\nEscolha um exemplo: ").strip().lower()
        
        if choice == '0':
            for name, func in examples:
                try:
                    func()
                except KeyboardInterrupt:
                    print("\nInterrompido pelo utilizador")
                    break
                except Exception as e:
                    print(f"\n✗ Erro: {e}")
                
                input("\nPressione Enter para continuar...")
            break
        
        elif choice == 'q':
            print("Sair...")
            break
        
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            idx = int(choice) - 1
            try:
                examples[idx][1]()
            except KeyboardInterrupt:
                print("\nInterrompido pelo utilizador")
            except Exception as e:
                print(f"\n✗ Erro: {e}")
            
            input("\nPressione Enter para voltar ao menu...")
        
        else:
            print("✗ Opção inválida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSair...")
    except Exception as e:
        print(f"\nErro: {e}")
        import traceback
        traceback.print_exc()
