import pygame
import sys
from Game import Game

if __name__ == "__main__":
    try:
        pygame.init()
        print("Iniciando motor do jogo...")
        game = Game()
        print("Janela criada com sucesso. Rodando...")
        game.run()
    except Exception as e:
        print("\n--- ERRO DETECTADO ---")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem: {e}")
        import traceback
        traceback.print_exc()
        print("----------------------")
        input("Pressione Enter para fechar...")