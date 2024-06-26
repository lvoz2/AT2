import multiprocessing as mp
import os
import pathlib
import sys
from typing import Any, Callable, Optional, Sequence

import pygame

import element
import event_processors
import events
import scene
import singleton
import sprite


class Display(metaclass=singleton.Singleton):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
        draw_async: bool = False,
        num_processes: Optional[int] = None,
    ) -> None:
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
            self.draw_async = draw_async
            self.num_processes = num_processes

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
        # self.draw_process.shutdown()
        pass

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        if self.cur_screen is not None:
            self.delta.append(self.clock.tick(25))
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.window.fill([0, 0, 0])
            self.cur_screen.design.rect = self.window.blit(
                self.cur_screen.design.surf,
                pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]),
            )
            if self.cur_screen.elements != [None]:
                if self.draw_async:
                    func: Callable[[tuple["Display", element.Element]], None] = (
                        lambda args: args[1].draw(args[0])
                    )
                    num_processes: Optional[int] = None
                    if self.num_processes is None:
                        num_processes = os.cpu_count()
                    else:
                        num_processes = self.num_processes
                    if num_processes is None:
                        raise ValueError("Number of processes cannot be None")
                    print(num_processes)
                    with mp.Pool(processes=num_processes) as draw_pool:
                        for element_layer in self.cur_screen.elements:
                            print("Test")
                            iter_layer: list[tuple["Display", element.Element]] = [
                                (self, e) for e in element_layer
                            ]
                            size: int = len(element_layer) // num_processes
                            print(iter_layer)
                            print(size)
                            draw_pool.imap_unordered(
                                func,
                                iter_layer,
                                size,
                            )
                            print("End")
                else:
                    for element_layer in self.cur_screen.elements:
                        for e in element_layer:
                            e.draw(self)
            self.update(self.delta)
            pygame.display.flip()
