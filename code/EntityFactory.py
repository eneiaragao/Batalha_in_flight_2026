import pygame
import os
from Player import Player
from Enemy import Enemy

class EntityFactory:
    @staticmethod
    def get_entity(entity_type, x, y, extra_info=None, player_id=1):
        """
        entity_type: "player" ou "enemy"
        extra_info: Recebe o PlaneConfig (para Player) ou a Velocidade (para Enemy).
        """
        if entity_type == "player":
            # Retorna o Player. A lógica de qual imagem usar está no PlaneConfig
            return Player(x, y, extra_info, player_id)

        elif entity_type == "enemy":
            # extra_info é a velocidade definida no Level_Config
            speed = extra_info if extra_info is not None else 3
            return Enemy(x, y, speed)

        return None