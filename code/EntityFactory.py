import pygame
import os


class EntityFactory:
    @staticmethod
    def get_entity(entity_type, x, y, extra_info=None):
        # Define o caminho base da pasta de assets
        asset_path = "./asset/"

        if entity_type == "player":
            # extra_info seria o objeto PlaneConfig escolhido
            img_path = os.path.join(asset_path, f"{extra_info.asset_name}.png")
            sprite = pygame.image.load(img_path).convert_alpha()
            # Retorna o objeto Player já com a imagem (sprite)
            from Player import Player
            return Player(x, y, extra_info, sprite)

        elif entity_type == "enemy":
            # Escolhe aleatoriamente entre Enemy1 ou Enemy2
            import random
            enemy_img = random.choice(["Enemy1", "Enemy2"])
            img_path = os.path.join(asset_path, f"{enemy_img}.png")
            sprite = pygame.image.load(img_path).convert_alpha()
            from Enemy import Enemy
            return Enemy(x, y, extra_info, sprite)  # extra_info aqui é a velocidade