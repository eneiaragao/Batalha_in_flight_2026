import sys
import os
import pygame

# Detecta se está rodando como script ou como executável (.exe)
if getattr(sys, 'frozen', False):
    # Se for executável, a pasta base é onde o .exe está
    base_dir = os.path.dirname(sys.executable)
else:
    # Se for script (PyCharm), a pasta base é onde o Main.py está
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Adiciona a pasta 'code' ao sys.path de forma absoluta
code_dir = os.path.join(base_dir, "code")
if code_dir not in sys.path:
    sys.path.insert(0, code_dir)

# Agora o import deve funcionar
try:
    from Game import Game
except Exception as e:
    print(f"\nErro ao importar Game: {e}")
    # Mostra onde o Python está procurando
    print(f"Pasta de busca atual: {code_dir}")
    input("Pressione Enter para sair...")
    sys.exit()

# 3. Execução Principal
if __name__ == "__main__":
    try:
        pygame.init()
        print("Iniciando Battle In Flight 2026...")

        game = Game()
        game.run()

    except Exception as e:
        print(f"\n--- ERRO DURANTE A EXECUÇÃO ---")
        print(f"Mensagem: {e}")
        import traceback

        traceback.print_exc()
        input("\nPressione Enter para fechar...")