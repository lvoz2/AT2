from typing import Any, Callable, Iterator, Optional

import pygame

import element
import sprite


class Scene(element.Element):
    def __init__(self, bground: sprite.Sprite) -> None:
        super().__init__(bground)
        self.renderables = None
        self.elements: list[list[element.Element]] = [[]]
        self.all_listeners: Optional[
            dict[
                int,
                dict[
                    Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]
                ],
            ]
        ] = None

    @property
    def visible_elements(self) -> Iterator[element.Element]:
        for element_layer in self.elements:
            for e in element_layer:
                if e.visible:
                    yield e

    def get_all_listeners(self) -> None:
        listeners: dict[
            int,
            dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]],
        ] = self.listeners
        for layer in self.elements:
            for e in layer:
                for event_type, listeners_dict in e.listeners.items():
                    if event_type not in listeners:
                        listeners[event_type] = {}
                    for callback, options in listeners_dict.items():
                        listeners[event_type][callback] = options
        self.all_listeners = listeners
