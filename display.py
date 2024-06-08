import sys
from typing import Optional, Sequence
import pygame
import screen
import singleton


class Display(metaclass=singleton.Singleton):
    def __init__(self, dim: Sequence[int] = (800, 600)) -> None:
        if not hasattr(self, "created"):
            self.screens: dict[str, screen.Screen] = {}
            self.cur_screen: Optional[screen.Screen] = None
            pygame.init()
            self.window = pygame.display.set_mode(dim)
            pygame.key.set_repeat(500, 50)
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            self.game_over: bool = False
            self.created: bool = True

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            self.cur_screen = self.screens[new_screen]
        else:
            raise KeyError(
                f'Screen with identifier "{new_screen}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_screen(self, name: str, new_screen: screen.Screen) -> bool:
        if name not in self.screens:
            self.screens[name] = new_screen
        else:
            raise KeyError(
                "Screen couldn't be added, becuase another Screen with the "
                "same name already loaded. Find a different name and try again"
            )
        return name in self.screens

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                match (e.type):
                    case pygame.KEYDOWN:
                        items = self.cur_screen.active_keys.items()
                        for keys, values in items:
                            combo: dict[str, int] = {
                                "key": e.key,
                                "mods": e.mod,
                            }
                            if combo in keys:
                                values[1](values[2]["args"], values[2]["kwargs"])
                    case pygame.MOUSEBUTTONDOWN:
                        for el, vals in self.cur_screen.clickables.items():
                            if el.rect.collidepoint(e.pos):
                                vals[1](vals[2]["args"], vals[2]["kwargs"])
                    case _:
                        pass

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        if self.cur_screen is not None:
            self.delta.append(self.clock.tick())
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
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
