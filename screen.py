import pygame


class Screen:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        self.state = "menu"
