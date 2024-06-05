import pygame


class Surf_Rect:
    def __init__(self, surf: pygame.Surface, rect: pygame.Rect) -> None:
        self.surf = surf
        self.rect = rect
