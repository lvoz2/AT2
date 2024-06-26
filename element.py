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
            int,
            dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]],
        ] = {}
        self.visible = visible

    def register_listener(
        self,
        event_type: int,
        func: Callable[[pygame.event.Event, dict[str, Any]], None],
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
        func: Callable[[pygame.event.Event, dict[str, Any]], None],
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
        print("called")
        self.visible = (
            (0 - self.design.rect.width) < self.design.rect.x < window.dimensions[0]
        ) and (
            (0 - self.design.rect.height) < self.design.rect.y < window.dimensions[1]
        )
        if self.visible:
            new_rect: pygame.Rect = window.window.blit(
                self.design.surf, self.design.rect, self.mask
            )
            self.design.rect.x, self.design.rect.y = new_rect.x, new_rect.y
