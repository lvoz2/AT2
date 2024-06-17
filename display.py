import sys
from typing import Optional, Sequence
import pygame
import events
import event_processors
import scene
import singleton


class Display(metaclass=singleton.Singleton):
    def __init__(self, dim: Sequence[int] = (800, 600)) -> None:
        if not hasattr(self, "created"):
            self.screens: dict[str, scene.Scene] = {}
            self.cur_screen: Optional[scene.Scene] = None
            pygame.init()
            self.window = pygame.display.set_mode(dim)
            pygame.key.set_repeat(500, 50)
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            self.game_over: bool = False
            self.__events = events.Events()
            event_processors.load()
            self.created: bool = True

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            event_processor: events.Events = events.Events()
            event_processor.cur_screen = self.screens[new_screen]
            self.cur_screen = self.screens[new_screen]
        else:
            raise KeyError(
                f'Screen with identifier "{new_screen}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_screen(self, name: str, new_screen: scene.Scene) -> bool:
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
                self.__events.notify(e)

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        if self.cur_screen is not None:
            self.delta.append(self.clock.tick())
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.window.fill([0, 0, 0])
            self.window.blit(self.cur_screen.design, [0, 0])
            if self.cur_screen.elements != [None]:
                for element_layer in self.cur_screen.elements:
                    for element in element_layerr:
                        element.draw(self.window)
            self.update(self.delta)
            pygame.display.flip()
