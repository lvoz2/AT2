import pygame
import screen
from singleton import Singleton


class Display(metaclass=Singleton):
    def __init__(self, cur_screen: str, scr: screen.Screen) -> None:
        self.screens: dict[str, screen.Screen] = {cur_screen: scr}
        self.cur_screen = self.screens[cur_screen]
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta: list[int] = [0]
        self.game_over: bool = False

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            self.cur_screen = self.screens[new_screen]
        else:
            raise KeyError("Screen not found, either because it does not exist or hasn't been loaded into the Display")

    def handle_events(self) -> None:
        keys = pygame.key.get_pressed()
        for key in self.cur_screen.active_keys.keys():
            if key in keys:
                self.cur_screen.active_keys[key]()

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        self.delta.append(self.clock.tick())
        if len(self.delta) > 10:
            self.delta = self.delta[(len(self.delta) - 10):]
        self.window.fill([0, 0, 0])
        self.window.blit(self.cur_screen.bground, [0, 0])
        if self.cur_screen.entities != [None]:
            for entity in self.cur_screen.entities:
                entity.draw(self.window)
        if self.cur_screen.ui != [None]:
            for e in self.cur_screen.ui:
                e.draw(self.window)
        self.handle_events()
        self.update(self.delta)
        pygame.display.flip()
