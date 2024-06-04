import pygame
import character


class Enemy(character.Character):
    def __init__(self, surf: pygame.Surface, x: int, y: int, name: str, health_regen_speed: float = 1, scale: int = 1, defense: int = 10, mana: int = 10, strength: int = 10):
        super().__init__(surf, x, y, name, health_regen_speed, scale, defense, mana, strength)
