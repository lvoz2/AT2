import pygame
from player import Player
from assets import GAME_ASSETS


class Mage(Player):
    def __init__(self, x: int, y: int, window: pygame.Surface, name: str, scale: int = 1) -> None:
        super().__init__(GAME_ASSETS["mage"], x, y, window, name, "mage", scale, mana=15)
