import sys
from typing import Optional, Sequence
import pygame
import screen
import singleton


class Display(metaclass=singleton.Singleton):
    def __init__(self, dim: Sequence[int] = (800, 600)) -> None:
        self.screens: dict[str, screen.Screen] = {}
        self.cur_screen: Optional[screen.Screen] = None
        pygame.init()
        self.window = pygame.display.set_mode(dim)
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.delta: list[int] = [0]
        self.game_over: bool = False

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            self.cur_screen = self.screens[new_screen]
        else:
            raise KeyError("Screen not found, either because it does not exist or hasn't been loaded into the Display")

    def add_screen(self, name: str, new_screen: screen.Screen) -> None:
        if name not in self.screens:
            self.screens[name] = new_screen
        else:
            raise KeyError("Screen couldn't be added, becuase another Screen with the same name already loaded. Find a different name and try again.")

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                match (e.type):
                    case pygame.KEYDOWN:
                        for keys in self.cur_screen.active_keys.keys():
                            combo: dict[str, int] = {"key": e.key, "mods": e.mod}
                            if combo in keys:
                                self.cur_screen.active_keys[keys][1](self.cur_screen.active_keys[keys][2]["args"], self.cur_screen.active_keys[keys][2]["kwargs"])
                    case pygame.MOUSEBUTTONDOWN:
                        for el in self.cur_screen.clickables.keys():
                            if el.get_rect().collidepoint(e.pos):
                                self.cur_screen.clickables[el][1](self.cur_screen.clickables[el][2]["args"], self.cur_screen.clickables[el][2]["kwargs"])
                    case _:
                        pass

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        if self.cur_screen is not None:
            self.delta.append(self.clock.tick())
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10):]
            self.window.fill([0, 0, 0])
            self.window.blit(self.cur_screen.bground, [0, 0])
            if self.cur_screen.entities != [None]:
                for entity_layer in self.cur_screen.entities:
                    for entity in entity_layer:
                        entity.draw(self.window)
            if self.cur_screen.ui != [None]:
                for ui_layer in self.cur_screen.ui:
                    for ui_e in ui_layer:
                        ui_e.draw(self.window)
            self.update(self.delta)
            pygame.display.flip()
