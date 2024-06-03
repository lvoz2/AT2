import pygame
import screen
from singleton import Singleton


class Display(metaclass=Singleton):
    def __init__(self, cur_screen: str, scr: screen.Screen) -> None:
        self.screens: dict[str, screen.Screen] = {cur_screen: scr}
        self.cur_screen = cur_screen
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            self.cur_screen = new_screen
        else:
            raise KeyError("Screen not found, either because it does not exist or hasn't been loaded into the Display")

    def draw(self) -> None:
        pass
