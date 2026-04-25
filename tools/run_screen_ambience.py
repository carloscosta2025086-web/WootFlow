"""
Exemplo de uso do Screen Ambience
Executa o perfil Screen Ambience com o teclado Wooting RGB
"""

import sys
import time
import os

try:
    from wooting_rgb import WootingRGB
    from screen_ambience_profile import load_ambience_profile
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Certifique-se de que wooting_rgb está instalado e configurado.")
    sys.exit(1)


def print_banner():
    print("\n" + "=" * 60)
    print("  🎨 Screen Ambience - RGB Ambilight para Teclado Wooting")
    print("=" * 60)
    print()


def print_menu():
    print("\nOpções:")
    print("  1 - Modo Cinemático (suave, 30 FPS)")
    print("  2 - Modo Dinâmico (rápido, 60 FPS)")
    print("  3 - Modo Gaming (ultra-rápido, 120 FPS)")
    print("  4 - Ajustar brilho")
    print("  5 - Ver estatísticas")
    print("  6 - Pausar/Retomar")
    print("  q - Sair")
    print()


def main():
    print_banner()
    
    # Conectar ao teclado
    print("Inicializando teclado Wooting RGB...")
    try:
        kb = WootingRGB()
    except FileNotFoundError as e:
        print(f"ERRO: {e}")
        print("Veja o README.md para instruções de instalação.")
        sys.exit(1)
    
    if not kb.is_connected():
        print("ERRO: Teclado Wooting não encontrado!")
        print("Verifique se o teclado está conectado.")
        sys.exit(1)
    
    info = kb.get_device_info()
    if info:
        print(f"✓ Conectado: {info['model']}")
        print(f"  Linhas: {info['max_rows']}, Colunas: {info['max_columns']}")
    else:
        print("✓ Teclado Wooting conectado!")
    print()
    
    # Carregar perfil Screen Ambience
    print("Carregando perfil Screen Ambience...")
    try:
        profile = load_ambience_profile(kb)
        print("✓ Perfil carregado")
    except FileNotFoundError as e:
        print(f"ERRO: {e}")
        sys.exit(1)
    except ImportError:
        print("ERRO: Módulo PIL ou mss não encontrado.")
        print("Instale com: pip install Pillow mss")
        sys.exit(1)
    
    print()
    
    # Ativar perfil
    print("Ativando perfil Screen Ambience...")
    try:
        profile.activate()
        print("✓ Perfil ativo!\n")
        print("O teclado agora está replicando as cores do seu ecrã em tempo real.")
        print("Mudanças de cores aparecem refletidas nos LEDs.")
        print()
    except Exception as e:
        print(f"ERRO ao ativar perfil: {e}")
        sys.exit(1)
    
    # Loop interativo
    try:
        paused = False
        
        while True:
            print_menu()
            choice = input("Escolha uma opção: ").strip().lower()
            
            if choice == "1":
                profile.set_mode("cinematic")
                profile.print_status()
            
            elif choice == "2":
                profile.set_mode("dynamic")
                profile.print_status()
            
            elif choice == "3":
                profile.set_mode("gaming")
                profile.print_status()
            
            elif choice == "4":
                try:
                    brightness = float(input("Brilho (0.0 a 2.0): "))
                    profile.set_brightness(brightness)
                except ValueError:
                    print("Valor inválido!")
            
            elif choice == "5":
                profile.print_status()
            
            elif choice == "6":
                if paused:
                    print("Retomando...")
                    profile.activate()
                    paused = False
                else:
                    print("Pausando...")
                    profile.deactivate()
                    paused = True
            
            elif choice == "q":
                print("\nDesativando Screen Ambience...")
                break
            
            else:
                print("Opção inválida!")
    
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo utilizador")
    
    finally:
        # Cleanup
        profile.deactivate()
        print("✓ Perfil desativado")
        print("\nObrigado por usar Screen Ambience! 🎨\n")


if __name__ == "__main__":
    main()
