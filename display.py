import concurrent.futures as cf
import multiprocessing as mp
import pathlib
import sys
from typing import Any, Optional, Sequence

import pygame

import event_processors
import events
import scene
import singleton
import sprite


class Display(metaclass=singleton.Singleton):
    def __init__(self, title: str = "", dim: Sequence[int] = (0, 0)) -> None:
        if not hasattr(self, "created"):
            self.dimensions = dim
            self.screens: dict[str, scene.Scene] = {}
            self.cur_screen: Optional[scene.Scene] = None
            pygame.init()
            self.window = pygame.display.set_mode(dim)
            pygame.display.set_caption(title)
            pygame.key.set_repeat(25)
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            self.game_over: bool = False
            self.events = events.Events()
            event_processors.load()
            self.created: bool = True
            self.custom_events: dict[str, int] = {
                "dmg_event": pygame.event.custom_type(),
                "keypress": pygame.event.custom_type(),
            }
            self.draw_process: cf.ProcessPoolExecutor = cf.ProcessPoolExecutor(
                max_workers=1
            )

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
                "Scene couldn't be added, becuase another Scene with the same name "
                f"already loaded. Find a different name and try again. Name: {name}"
            )
        return name in self.screens

    def quit(self) -> None:
        self.draw_process.shutdown()

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw_process.submit(self.draw, self)
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self, window: "display.Display") -> None:
        if window.cur_screen is not None:
            window.delta.append(window.clock.tick(25))
            if len(window.delta) > 10:
                window.delta = window.delta[(len(window.delta) - 10) :]
            window.window.fill([0, 0, 0])
            window.cur_screen.design.rect = window.window.blit(
                window.cur_screen.design.surf,
                pygame.Rect(0, 0, window.dimensions[0], window.dimensions[1]),
            )
            if window.cur_screen.elements != [None]:
                for element_layer in window.cur_screen.elements:
                    # Do the pool here. Use imap(lambda element: element.draw(window), element_layer)
                    for element in element_layer:
                        element.draw(window)
            window.update(window.delta)
            pygame.display.flip()
