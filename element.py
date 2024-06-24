from typing import TYPE_CHECKING, Any, Callable, Optional, Sequence

import pygame

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
        self.design = design
        self.mask = mask
        self.listeners: dict[
            int, dict[Callable[..., None], Optional[dict[str, Any]]]
        ] = {}
        self.x = self.design.rect.x
        self.y = self.design.rect.y
        self.visible = visible

    def register_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = {}
        if options is None:
            options = {}
        options["target"] = self
        self.listeners[event_type][func] = options

    def deregister_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type not in self.listeners:
            raise KeyError(
                "No event listeners created yet for event type "
                f"{event_type}. Function: {func}"
            )
        if func not in self.listeners[event_type]:
            raise KeyError(
                "Event listener does not exist. Event Type: "
                f"{event_type}, Function: {func}"
            )
        if self.listeners[event_type][func] != options:
            raise ValueError(
                "The options argument provided did not match what was expected. "
                f"Expected {self.listeners[event_type][func]}, "
                f"received {options}"
            )
        del self.listeners[event_type][func]

    def draw(self, window: "display.Display") -> None:
        if self.visible:
            if ((0 - self.design.rect.width) < self.x < window.dimensions[0]) and (
                (0 - self.design.rect.height) < self.y < window.dimensions[1]
            ):
                self.design.rect = window.window.blit(
                    self.design.surf, self.design.rect, self.mask
                )
            else:
                self.visible = False
