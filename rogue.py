from character import Character
import pygame
from assets import GAME_ASSETS

class Rogue(Character):
    def __init__(self, x: int, y: int, window: pygame.Surface, name: str, scale: int=1):
        super().__init__(GAME_ASSETS["rogue"], x, y, window, name, "rogue", scale, defense=15)
        # Additional attributes and methods specific to the Rogue class
