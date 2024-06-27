import multiprocessing as mp
import multiprocessing.pool as mp_pool
import multiprocessing.synchronize as mp_sync
import time
from typing import Any, Optional, Sequence

import pygame

import event_processors
import events
import scene
import singleton


class DrawProps(metaclass=singleton.Singleton):
    def __init__(self, dim: Sequence[int] = (0, 0)) -> None:
        if not hasattr(self, "created"):
            self.__scenes: list[mp_sync.Lock | dict[str, scene.Scene]] = [mp.Lock(), {}]
            self.__cur_scene: list[mp_sync.Lock | Optional[scene.Scene]] = [
                mp.Lock(),
                None,
            ]
            self.__clock: list[mp_sync.Lock | pygame.time.Clock] = [
                mp.Lock(),
                pygame.time.Clock(),
            ]
            self.__delta: list[mp_sync.Lock | list[int]] = [mp.Lock(), [0]]
            self.__dimensions: list[mp_sync.Lock | Sequence[int]] = [mp.Lock(), dim]
            self.__window: list[mp_sync.Lock | pygame.Surface] = [
                mp.Lock(),
                pygame.display.set_mode(dim),
            ]
            self.created: bool = True

    # Accessors with locks
    @property
    def scenes(self) -> dict[str, scene.Scene]:
        if isinstance(self.__scenes[0], mp_sync.Lock) and isinstance(
            self.__scenes[1], dict
        ):
            with self.__scenes[0] as lock:
                return self.__scenes[1]
        raise TypeError("__scenes has the wrong types")

    @scenes.setter
    def scenes(self, new_scenes: dict[str, scene.Scene]) -> None:
        if isinstance(self.__scenes[0], mp_sync.Lock):
            with self.__scenes[0] as lock:
                self.__scenes[1] = new_scenes

    @property
    def cur_scene(self) -> Optional[scene.Scene]:
        if isinstance(self.__cur_scene[0], mp_sync.Lock) and (
            isinstance(self.__cur_scene[1], scene.Scene) or self.__cur_scene[1] is None
        ):
            with self.__cur_scene[0] as lock:
                return self.__cur_scene[1]
        raise TypeError("__cur_scene has the wrong types")

    @cur_scene.setter
    def cur_scene(self, new_scene: Optional[scene.Scene]) -> None:
        if isinstance(self.__cur_scene[0], mp_sync.Lock):
            with self.__cur_scene[0] as lock:
                self.__cur_scene[1] = new_scene

    @property
    def clock(self) -> pygame.time.Clock:
        if isinstance(self.__clock[0], mp_sync.Lock) and isinstance(
            self.__clock[1], pygame.time.Clock
        ):
            with self.__clock[0] as lock:
                return self.__clock[1]
        raise TypeError("__clock has the wrong types")

    @clock.setter
    def clock(self, new_clock: pygame.time.Clock) -> None:
        if isinstance(self.__clock[0], mp_sync.Lock):
            with self.__clock[0] as lock:
                self.__clock[1] = new_clock

    @property
    def delta(self) -> list[int]:
        if isinstance(self.__delta[0], mp_sync.Lock) and isinstance(
            self.__delta[1], list
        ):
            with self.__delta[0] as lock:
                return self.__delta[1]
        raise TypeError("__delta has the wrong types")

    @delta.setter
    def delta(self, new_delta: list[int]) -> None:
        if isinstance(self.__delta[0], mp_sync.Lock):
            with self.__delta[0] as lock:
                self.__delta[1] = new_delta

    @property
    def window(self) -> pygame.Surface:
        if isinstance(self.__window[0], mp_sync.Lock) and isinstance(
            self.__window[1], pygame.Surface
        ):
            with self.__window[0] as lock:
                return self.__window[1]
        raise TypeError("__window has the wrong types")

    @window.setter
    def window(self, new_window: pygame.Surface) -> None:
        if isinstance(self.__window[0], mp_sync.Lock):
            with self.__window[0] as lock:
                self.__window[1] = new_window

    @property
    def dimensions(self) -> Sequence[int]:
        if isinstance(self.__dimensions[0], mp_sync.Lock) and isinstance(
            self.__dimensions[1], Sequence
        ):
            with self.__dimensions[0] as lock:
                return self.__dimensions[1]
        raise TypeError("__dimensions has the wrong types")

    @dimensions.setter
    def dimensions(self, new_dimensions: Sequence[int]) -> None:
        if isinstance(self.__dimensions[0], mp_sync.Lock):
            with self.__dimensions[0] as lock:
                self.__dimensions[1] = new_dimensions

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self, inst: Optional["DrawProps"] = None) -> None:
        ctx: "DrawProps" = self if inst is None else inst
        if ctx.cur_scene is not None:
            ctx.delta.append(ctx.clock.tick(25))
            if len(ctx.delta) > 10:
                ctx.delta = ctx.delta[(len(ctx.delta) - 10) :]
            ctx.window.fill([0, 0, 0])
            ctx.cur_scene.design.rect = ctx.window.blit(
                ctx.cur_scene.design.surf,
                pygame.Rect(0, 0, ctx.dimensions[0], ctx.dimensions[1]),
            )
            if ctx.cur_scene.elements != [None]:
                for element_layer in ctx.cur_scene.elements:
                    for e in element_layer:
                        e.draw(ctx)
            ctx.update(ctx.delta)
            pygame.display.flip()


class Display(DrawProps, metaclass=singleton.Singleton):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
    ) -> None:
        if not hasattr(self, "created"):
            pygame.init()
            super().__init__(dim)
            pygame.display.set_caption(title)
            pygame.key.set_repeat(25)
            self.game_over: bool = False
            self.events = events.Events()
            event_processors.load()
            self.custom_events: dict[str, int] = {
                "dmg_event": pygame.event.custom_type(),
                "keypress": pygame.event.custom_type(),
            }

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.scenes:
            event_processor: events.Events = events.Events()
            event_processor.cur_screen = self.scenes[new_screen]
            self.cur_screen = (  # pylint: disable=attribute-defined-outside-init
                self.scenes[  # pylint: disable=attribute-defined-outside-init
                    new_screen  # pylint: disable=attribute-defined-outside-init
                ]  # pylint: disable=attribute-defined-outside-init
            )  # pylint: disable=attribute-defined-outside-init
        else:
            raise KeyError(
                f'Screen with identifier "{new_screen}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_screen(self, name: str, new_screen: scene.Scene) -> bool:
        if name not in self.scenes:
            self.scenes[name] = new_screen
        else:
            raise KeyError(
                "Scene couldn't be added, becuase another Scene with the same name "
                f"already loaded. Find a different name and try again. Name: {name}"
            )
        return name in self.scenes

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)


class AsyncDisplay(Display, metaclass=singleton.Singleton):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
    ) -> None:
        if not hasattr(self, "ready"):
            self.ready = False
            super().__init__(title, dim)
            self.ctx = mp.get_context("spawn")
            self.draw_process: mp_pool.Pool = mp.Pool(processes=1)
            self.ready = True

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw_process.apply_async(lambda data: data.draw(data), args=[self])
            self.cur_screen.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_screen.all_listeners)
            time.sleep(0.04)
