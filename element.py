from typing import Any, Callable, Optional, Sequence

import pygame

import sprite


class Element:
    def __init__(
        self,
        design: sprite.Sprite | str,
        mask: Optional[pygame.Rect] = None,
        visible: bool = False,
    ) -> None:
        elif isinstance(design, sprite.Sprite):
            self.design = design
        self.mask = mask
        
        self.listeners: dict[
            int, dict[Callable[..., None], Optional[dict[str, Any]]]
        ] = {}
        self.x = self.design.x
        self.y = self.design.y
        self.visible = visible
        self.rect_options = rect_options

    # def update_design(new_design)

    def __get_val_from_dict(
        self, dictionary: Optional[dict[Any, Any]], key: Any, default: Any = None
    ) -> Any:
        if dictionary is None:
            return default
        if key in dictionary:
            return dictionary[key]
        return default

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

    def draw(self, window: pygame.Surface) -> None:
        if self.__get_val_from_dict(self.rect_options, "center", False):
            self.design.rect.center = (self.x, self.y)
            self.design.rect = window.blit(
                self.design.surf, self.design.rect, self.mask
            )
        else:
            self.design.rect = window.blit(
                self.design.surf, [self.x, self.y], self.mask
            )
