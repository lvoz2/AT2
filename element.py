import concurrent.futures._base as cf_b
import concurrent.futures.process as cf_p
import multiprocessing as mp
import multiprocessing.synchronize as mp_sync
from typing import TYPE_CHECKING, Any, Callable, Literal, Optional, Sequence

import pygame

import draw_process_funcs as dpf
import events
import sprite

if TYPE_CHECKING:
    import display


class Element:
    def __init__(
        self,
        design: sprite.Sprite,
        mask: Optional[pygame.Rect] = None,
        visible: bool = False,
    ) -> None:
        self.__design: list[mp_sync.Lock | sprite.Sprite] = [mp.Lock(), design]
        self.mask = mask
        self.listeners: dict[
            int,
            dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]],
        ] = {}
        self.visible = visible
        self.bytes: tuple[
            bytes, Sequence[int], Literal["P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA"]
        ] = (
            pygame.image.tobytes(self.design.surf, "RGBA"),
            [self.design.width, self.design.height],
            "RGBA",
        )

    @property
    def design(self) -> sprite.Sprite:
        if isinstance(self.__design[0], mp_sync.Lock) and isinstance(
            self.__design[1], sprite.Sprite
        ):
            with self.__design[0] as lock:  # pylint: disable=unused-variable
                return self.__design[1]
        raise TypeError("__design has the wrong types")

    @design.setter
    def design(self, new_design: sprite.Sprite) -> None:
        if isinstance(self.__design[0], mp_sync.Lock):
            with self.__design[0] as lock:  # pylint: disable=unused-variable
                self.__design[1] = new_design
                self.bytes = (
                    pygame.image.tobytes(self.design.surf, "RGBA"),
                    [self.design.width, self.design.height],
                    "RGBA",
                )

    def register_listener(
        self,
        event_type: int | str,
        func: Callable[[pygame.event.Event, dict[str, Any]], None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if isinstance(event_type, str):
            evts: events.Events = events.Events()
            evt_type: int = evts.get_event_id(event_type)
        else:
            evt_type = event_type
        if evt_type not in self.listeners:
            self.listeners[evt_type] = {}
        if options is None:
            options = {}
        options["target"] = self
        self.listeners[evt_type][func] = options

    def deregister_listener(
        self,
        event_type: int | str,
        func: Callable[[pygame.event.Event, dict[str, Any]], None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if isinstance(event_type, str):
            evts: events.Events = events.Events()
            evt_type: int = evts.get_event_id(event_type)
        else:
            evt_type = event_type
        if evt_type not in self.listeners:
            raise KeyError(
                "No event listeners created yet for event type "
                f"{evt_type}. Function: {func}"
            )
        if func not in self.listeners[evt_type]:
            raise KeyError(
                "Event listener does not exist. Event Type: "
                f"{evt_type}, Function: {func}"
            )
        if self.listeners[evt_type][func] != options:
            raise ValueError(
                "The options argument provided did not match what was expected. "
                f"Expected {self.listeners[evt_type][func]}, "
                f"received {options}"
            )
        del self.listeners[evt_type][func]

    def update_rect(self, future: cf_b.Future) -> None:
        res: pygame.Rect = future.result(0.01)
        self.design.x, self.design.y = res.x, res.y

    def draw_async(
        self,
        executor: cf_p.ProcessPoolExecutor,
        dimensions: Sequence[int],
    ) -> None:
        self.visible = ((0 - self.design.width) < self.design.x < dimensions[0]) and (
            (0 - self.design.height) < self.design.y < dimensions[1]
        )
        if self.visible:
            future: cf_b.Future = executor.submit(
                dpf.construct_and_blit,
                (
                    self.bytes[0],
                    self.bytes[1],
                    self.bytes[2],
                ),
                self.design.rect,
                self.mask,
            )
            future.add_done_callback(self.update_rect)

    def draw(self, window: "display.DrawProps") -> None:
        self.visible = (
            (0 - self.design.width) < self.design.x < window.dimensions[0]
        ) and ((0 - self.design.height) < self.design.y < window.dimensions[1])
        if self.visible:
            new_rect: pygame.Rect = window.window.blit(
                self.design.surf, self.design.rect, self.mask
            )
            self.design.x, self.design.y = new_rect.x, new_rect.y
