# import concurrent.futures as cf
import concurrent.futures._base as cf_b
import concurrent.futures.process as cf_p
import multiprocessing as mp
import multiprocessing.synchronize as mp_sync
import time
from typing import Any, Optional, Sequence

import pygame

import draw_process_funcs as dpf
import element
import events
import scene
import sprite
import utils


class DrawProps(element.Element, metaclass=utils.Singleton):
    def __init__(
        self,
        dim: Sequence[int] = (0, 0),
        from_async: bool = False,
    ) -> None:
        if not hasattr(self, "__built"):
            self.__cur_scene: list[mp_sync.Lock | Optional[scene.Scene]] = [
                mp.Lock(),
                None,
            ]
            self.events = events.Events()
            self.__dimensions: list[mp_sync.Lock | Sequence[int]] = [mp.Lock(), dim]
            if not from_async:
                self.__window: list[mp_sync.Lock | pygame.Surface] = [
                    mp.Lock(),
                    pygame.display.set_mode(dim),
                ]
            super().__init__(
                sprite.Sprite(
                    rect=pygame.Rect(0, 0, dim[0], dim[1]),
                    rect_options={"colour": [0, 0, 0]},
                )
            )
            self.from_async = from_async
            self.executor: Optional[cf_p.ProcessPoolExecutor] = None
            self.__built: bool = True  # pylint: disable=unused-private-member

    # Accessors with locks
    @property
    def cur_scene(self) -> Optional[scene.Scene]:
        if isinstance(self.__cur_scene[0], mp_sync.Lock) and (
            isinstance(self.__cur_scene[1], scene.Scene) or self.__cur_scene[1] is None
        ):
            with self.__cur_scene[0] as lock:  # pylint: disable=unused-variable
                return self.__cur_scene[1]
        raise TypeError(
            f"__cur_scene has the wrong types. Type: {type(self.__cur_scene[1])}"
        )

    @cur_scene.setter
    def cur_scene(self, new_scene: scene.Scene) -> None:
        if isinstance(self.__cur_scene[0], mp_sync.Lock):
            with self.__cur_scene[0] as lock:  # pylint: disable=unused-variable
                self.__cur_scene[1] = new_scene
                self.events.cur_scene = new_scene

    @cur_scene.deleter
    def cur_scene(self) -> None:
        del self.__cur_scene

    @property
    def window(self) -> pygame.Surface:
        try:
            if isinstance(self.__window[0], mp_sync.Lock) and isinstance(
                self.__window[1], pygame.Surface
            ):
                with self.__window[0] as lock:  # pylint: disable=unused-variable
                    return self.__window[1]
        except AttributeError as e:
            raise AttributeError(
                "The requested window does not exist in the main thread"
            ) from e
        raise TypeError("__window has the wrong types")

    @window.setter
    def window(self, new_window: pygame.Surface) -> None:
        if isinstance(self.__window[0], mp_sync.Lock):
            with self.__window[0] as lock:  # pylint: disable=unused-variable
                self.__window[1] = new_window

    @window.deleter
    def window(self) -> None:
        del self.__window

    @property
    def dimensions(self) -> Sequence[int]:
        if isinstance(self.__dimensions[0], mp_sync.Lock) and isinstance(
            self.__dimensions[1], Sequence
        ):
            with self.__dimensions[0] as lock:  # pylint: disable=unused-variable
                return self.__dimensions[1]
        raise TypeError("__dimensions has the wrong types")

    @dimensions.setter
    def dimensions(self, new_dimensions: Sequence[int]) -> None:
        if isinstance(self.__dimensions[0], mp_sync.Lock):
            with self.__dimensions[0] as lock:  # pylint: disable=unused-variable
                self.__dimensions[1] = new_dimensions

    @dimensions.deleter
    def dimensions(self) -> None:
        del self.__dimensions


class Display(DrawProps, metaclass=utils.Singleton):
    def __init__(
        self,
        title: str = "",
        dim: Sequence[int] = (0, 0),
        key_press_initial_delay: int = 0,
        key_press_interval: int = 0,
        from_async: bool = False,
    ) -> None:
        if not hasattr(self, "created"):
            self.created: bool = True
            self.scenes: dict[str, scene.Scene] = {}
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            if not from_async:
                pygame.init()
            super().__init__(dim=dim, from_async=from_async)
            pygame.display.set_caption(title)
            self.game_over: bool = False
            self.__key_press_leftover_delta: int = 0
            if not from_async:
                self.events.set_key_repeat(key_press_initial_delay, key_press_interval)

    def set_scene(self, new_scene: str, no_event: bool = False) -> None:
        if new_scene in self.scenes:
            if no_event:
                self.cur_scene = self.scenes[new_scene]
                return
            if self.cur_scene is None:
                evt: pygame.event.Event = pygame.event.Event(
                    self.events.event_types["switch_scene"],
                    new_scene=(new_scene, self.scenes[new_scene]),
                    old_scene=(None, None),
                )
            else:
                evt = pygame.event.Event(
                    self.events.event_types["switch_scene"],
                    new_scene=(new_scene, self.scenes[new_scene]),
                    old_scene=(
                        list(self.scenes.keys())[
                            list(self.scenes.values()).index(self.cur_scene)
                        ],
                        self.cur_scene,
                    ),
                )
            pygame.event.post(evt)
        else:
            raise KeyError(
                f'Scene with identifier "{new_scene}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_scene(
        self, name: str, new_scene: scene.Scene, overwrite: bool = False
    ) -> bool:
        if name not in self.scenes or overwrite:
            self.scenes[name] = new_scene
        else:
            raise KeyError(
                "Scene couldn't be added, becuase another Scene with the same name "
                "already loaded, and you have specified not to overwrite it. "
                f"Find a different name and try again. Name: {name}"
            )
        return name in self.scenes

    def update(self, delta: list[int]) -> None:
        self.__key_press_leftover_delta = self.events.create_key_press_event(
            delta[len(delta) - 1] + self.__key_press_leftover_delta
        )

    def handle_events(self) -> None:
        if self.cur_scene is not None:
            self.draw(self)
            self.cur_scene.get_all_listeners(self)
            for e in pygame.event.get():
                if self.cur_scene is not None:
                    self.events.notify(e, self.cur_scene.all_listeners)
                if e.type == self.events.event_types["switch_scene"]:
                    if e.new_scene is not None:
                        self.cur_scene = e.new_scene[1]

    def draw(self, window: DrawProps) -> None:
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
            super().__init__(title=title, dim=dim, from_async=True)
            self.runner: utils.AsyncRunner = utils.AsyncRunner(
                "display", start_method=start_method, initfunc=dpf.init, initargs=(dim,)
            )
            self.executor = self.runner.executor
            self.dimensions = dim
            self.ready = True

    def event_callback(self, fut: cf_b.Future) -> None:
        if self.cur_scene is not None:
            events_list: list[tuple[int, dict[str, Any]]] = fut.result()
            for evt in events_list:
                self.events.notify(
                    pygame.event.Event(evt[0], evt[1]), self.cur_scene.all_listeners
                )

    def handle_events(self) -> None:
        if self.cur_scene is not None:
            self.draw(self)
            self.cur_scene.get_all_listeners(self)
            events_fut = self.runner.executor.submit(dpf.get_events)
            events_fut.add_done_callback(self.event_callback)
            time.sleep(0.04)

    def update_rect(self, future: cf_b.Future) -> None:
        if self.cur_scene is None:
            raise ValueError(
                "No scene set, please set this first with "
                "AsyncDisplay.set_scene(scene_name) first."
            )
        self.cur_scene.design.rect = future.result(0.05)

    def draw(self, window: DrawProps) -> None:
        if self.cur_scene is not None:
            self.delta.append(self.clock.tick(25))
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.runner.executor.submit(dpf.fill_screen, [0, 0, 0])
            if (
                self.cur_scene.design.surf.get_width() != self.dimensions[0]
                or self.cur_scene.design.surf.get_height() != self.dimensions[1]
            ):
                self.cur_scene.design.rect.update(
                    0, 0, self.dimensions[0], self.dimensions[1]
                )
                self.cur_scene.design.surf = pygame.transform.scale(
                    self.cur_scene.design.surf,
                    (
                        self.dimensions[0],
                        self.dimensions[1],
                    ),
                )
                self.cur_scene.bytes = (
                    pygame.image.tobytes(self.cur_scene.design.surf, "RGBA"),
                    [
                        self.cur_scene.design.width,
                        self.cur_scene.design.height,
                    ],
                    "RGBA",
                )
            screen_flush: cf_b.Future = self.runner.executor.submit(
                dpf.construct_and_blit,
                (
                    self.cur_scene.bytes[0],
                    self.cur_scene.bytes[1],
                    self.cur_scene.bytes[2],
                ),
                pygame.Rect(0, 0, self.dimensions[0], self.dimensions[1]),
            )
            screen_flush.add_done_callback(self.update_rect)
            if self.cur_scene.elements != [None]:
                for element_layer in self.cur_scene.elements:
                    for e in element_layer:
                        e.draw_async(self.runner.executor, self.dimensions)
            self.update(self.delta)
            self.runner.executor.submit(pygame.display.flip)
