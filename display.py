import multiprocessing as mp
import multiprocessing.synchronize as mp_sync
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

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self, inst: Optional["Display"] = None) -> None:
        ctx: Display = self if inst is None else inst
        if ctx.cur_screen is not None:
            ctx.delta.append(ctx.clock.tick(25))
            if len(ctx.delta) > 10:
                ctx.delta = ctx.delta[(len(ctx.delta) - 10) :]
            ctx.window.fill([0, 0, 0])
            ctx.cur_screen.design.rect = ctx.window.blit(
                ctx.cur_screen.design.surf,
                pygame.Rect(0, 0, ctx.dimensions[0], ctx.dimensions[1]),
            )
            if ctx.cur_screen.elements != [None]:
                for element_layer in ctx.cur_screen.elements:
                    for e in element_layer:
                        e.draw(ctx)
            ctx.update(ctx.delta)
            pygame.display.flip()


class AsyncDisplay(Display):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
    ) -> None:
        super().__init__(title, dim)
        self.lock: mp_sync.Lock = mp.Lock()
        self.conn, conn = mp.Pipe()
        self.ctx = mp.get_context("spawn")
        self.draw_process = self.ctx.Process(target=self.draw_async, name=f"draw_process_for_{title}", args=[conn])
        self.draw_process.start()
        self.draw_process.run()

    def draw_async(self, conn: mp.connection.Connection) -> None:
        running: bool = True
        while running:
            data: Any = conn.recv()
            if isinstance(data, tuple):
                running = data[0]
                if not running:
                    break
                if len(data) > 2:
                    if isinstance(data[1], AsyncDisplay) and isinstance(data[2], mp_sync.Lock):
                        with data[2] as l:
                            data[1].draw(data[1])
        conn.close()

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.conn.send((True, self, self.lock))
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)