from typing import Any, Callable, Optional
import pygame
import entity
import surf_rect
import ui_element


class Screen:
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.listeners: dict[
            int, dict[Callable[..., None], Optional[dict[str, Any]]]
        ] = {}
        self.__active_keys: dict[
            tuple[int, int], tuple[str, Callable[..., None], dict[str, Any]]
        ] = {}
        self.__clickables: dict[
            surf_rect.Surf_Rect,
            tuple[str, Callable[..., None], dict[str, Any]],
        ] = {}
        self.elements: list[list[entity.Entity | ui_element.UI_Element]] = [[]]

    def register_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
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
                f"Expected {self.__cur_screen.listeners[event_type][func]}, "
                f"received {options}"
            )
        del self.listeners[event_type][func]
