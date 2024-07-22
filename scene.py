import functools
from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional

import pygame

import element
import sprite

if TYPE_CHECKING:
    import display


class Scene(element.Element):
    def __init__(self, bground: sprite.Sprite) -> None:
        super().__init__(bground)
        self.renderables = None
        self.elements: list[list[element.Element]] = [[]]
        self.all_listeners: Optional[
            dict[
                int,
                dict[
                    Callable[
                        [pygame.event.Event, dict[str, Any]],
                        Optional[functools.partial[None]],
                    ],
                    list[dict[str, Any]],
                ],
            ]
        ] = None

    @property
    def visible_elements(self) -> Iterator[element.Element]:
        for element_layer in self.elements:
            for e in element_layer:
                if e.visible:
                    yield e

    def get_all_listeners(self, window: "display.Display") -> None:
        listeners: dict[
            int,
            dict[
                Callable[
                    [pygame.event.Event, dict[str, Any]],
                    Optional[functools.partial[None]],
                ],
                list[dict[str, Any]],
            ],
        ] = {}
        all_elements: list[list[element.Element]] = [[window, self]]
        all_elements.extend(self.elements)
        for layer in all_elements:
            for e in layer:
                for event_type, listeners_dict in e.listeners.items():
                    if event_type not in listeners:
                        listeners[event_type] = {}
                    for callback, options in listeners_dict.items():
                        if callback not in listeners[event_type]:
                            listeners[event_type][callback] = []
                        listeners[event_type][callback].append(options)
        self.all_listeners = listeners
