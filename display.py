import concurrent.futures as cf
import concurrent.futures._base as cf_b
import multiprocessing as mp
import multiprocessing.synchronize as mp_sync
import time
from typing import Optional, Sequence

import pygame

import event_processors
import events
import scene
import utils


class DrawProps(metaclass=utils.Singleton):
    def __init__(
        self,
        dim: Sequence[int] = (0, 0),
        from_async: bool = False,
        runner: Optional[utils.AsyncRunner] = None,
    ) -> None:
        if not hasattr(self, "created"):
            self.__cur_scene: list[mp_sync.Lock | Optional[scene.Scene]] = [
                mp.Lock(),
                None,
            ]
            self.__dimensions: list[mp_sync.Lock | Sequence[int]] = [mp.Lock(), dim]
            if not from_async:
                self.__window: list[mp_sync.Lock | pygame.Surface] = [
                    mp.Lock(),
                    pygame.display.set_mode(dim),
                ]
            else:
                if runner is None:
                    raise TypeError(
                        "A runner must be provided to do work asynchronously"
                    )
                future: cf_b.Future = runner.executor.submit(
                    pygame.display.set_mode, dim
                )
                cf.wait([future])
                print(future.result())
                self.__window: list[mp_sync.Lock | pygame.Surface] = [
                    mp.Lock(),
                    future.result(0.01),
                ]
                print(self.__window)
            self.created: bool = True

    # Accessors with locks
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


class Display(DrawProps, metaclass=utils.Singleton):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
        from_async: bool = False,
        runner: Optional[utils.AsyncRunner] = None,
    ) -> None:
        if not hasattr(self, "created"):
            self.scenes: dict[str, scene.Scene] = {}
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            if not from_async:
                pygame.init()
            super().__init__(dim=dim, from_async=from_async, runner=runner)
            pygame.display.set_caption(title)
            if not from_async:
                pygame.key.set_repeat(25)
            else:
                if runner is None:
                    raise TypeError(
                        "A runner must be provided to do work asynchronously"
                    )
                cf.wait(
                    [runner.executor.submit(pygame.key.set_repeat, 25)],
                    return_when=cf.ALL_COMPLETED,
                )
            self.game_over: bool = False
            self.events = events.Events()
            event_processors.load()
            self.custom_events: dict[str, int] = {
                "dmg_event": pygame.event.custom_type(),
                "keypress": pygame.event.custom_type(),
            }

    def set_scene(self, new_scene: str) -> None:
        if new_scene in self.scenes:
            event_processor: events.Events = events.Events()
            event_processor.cur_scene = self.scenes[new_scene]
            self.cur_scene = self.scenes[new_scene]
        else:
            raise KeyError(
                f'Scene with identifier "{new_scene}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_scene(self, name: str, new_scene: scene.Scene) -> bool:
        if name not in self.scenes:
            self.scenes[name] = new_scene
        else:
            raise KeyError(
                "Scene couldn't be added, becuase another Scene with the same name "
                f"already loaded. Find a different name and try again. Name: {name}"
            )
        return name in self.scenes

    def handle_events(self) -> None:
        if self.cur_scene is not None:
            self.draw()
            self.cur_scene.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_scene.all_listeners)

    def draw(self) -> None:
        if self.cur_scene is not None:
            self.delta.append(self.clock.tick(25))
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.window.fill([0, 0, 0])
            self.cur_scene.design.rect = self.window.blit(
                self.cur_scene.design.surf,
                pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]),
            )
            if self.cur_scene.elements != [None]:
                for element_layer in self.cur_scene.elements:
                    for e in element_layer:
                        e.draw(self)
            self.update(self.delta)
            pygame.display.flip()


class AsyncDisplay(Display, metaclass=utils.Singleton):
    def __init__(
        self, title: str = "", dim: Sequence[int] = (0, 0), start_method: str = "fork"
    ) -> None:
        if not hasattr(self, "ready"):
            self.ready = False
            pygame.init()
            pygame.display.init()
            self.runner: utils.AsyncRunner = utils.AsyncRunner(
                "display", start_method=start_method
            )
            cf.wait(
                [self.runner.executor.submit(pygame.init)], return_when=cf.ALL_COMPLETED
            )
            cf.wait(
                [self.runner.executor.submit(pygame.display.init)],
                return_when=cf.ALL_COMPLETED,
            )
            super().__init__(title=title, dim=dim, from_async=True, runner=self.runner)
            self.ready = True

    def handle_events(self) -> None:
        if self.cur_scene is not None:
            self.draw()
            self.cur_scene.get_all_listeners()
            for e in pygame.event.get():
                self.events.notify(e, self.cur_scene.all_listeners)
            time.sleep(0.04)

    def update_rect(self, future: cf_b.Future) -> None:
        if self.cur_scene is None:
            raise ValueError(
                "No scene set, please set this first with "
                "AsyncDisplay.set_scene(scene_name) first."
            )
        self.cur_scene.design.rect = future.result(0.05)

    def draw(self) -> None:
        if self.cur_scene is not None:
            self.delta.append(self.clock.tick(25))
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.runner.executor.submit(print, "Test")
            self.runner.executor.submit(self.window.fill, [0, 0, 0])
            screen_flush: cf_b.Future = self.runner.executor.submit(
                self.window.blit,
                self.cur_scene.design.surf,
                pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]),
            )
            screen_flush.add_done_callback(self.update_rect)
            if self.cur_scene.elements != [None]:
                for element_layer in self.cur_scene.elements:
                    for e in element_layer:
                        e.draw_async(self.runner.executor, self.window, self.dimensions)
            self.update(self.delta)
            self.runner.executor.submit(pygame.display.flip)
