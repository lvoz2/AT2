from character import Character
from assets import GAME_ASSETS
import pygame

class Mage(Character):
    def __init__(self, x: int, y: int, window: pygame.Surface, name: str, scale: int=1) -> :
        super().__init__(GAME_ASSETS["mage"], x, y, window, name, "mage", scale, mana=15)
        
