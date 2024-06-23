import sys
import warnings
from typing import Any, Callable, Optional

import pygame

import scene
import singleton

# The way events will be handled is heavily influenced by JavaScript, especially
# addEventListener and removeEventListener. The interface for it should share its state
# across all instantiations, and so it is a Singleton. This file should implement the
# Observer design pattern, albeit with a slight difference: Events are first processed a
# little bit, so that, for example, a MouseDown listener is only fired when its target
# is actually clicked, instead of every MouseDown Event.


class Events(metaclass=singleton.Singleton):
    def __init__(self) -> None:
        if not hasattr(self, "created"):
            self.created: bool = True
            self.__cur_screen: Optional[scene.Scene] = None
            self.__processors: dict[
                int,
                tuple[
                    Callable[
                        [
                            pygame.event.Event,
                            Callable[..., None],
                            Optional[dict[str, Any]],
                        ],
                        bool,
                    ],
                    Optional[dict[str, Any]],
                ],
            ] = {}

    @property
    def cur_screen(self) -> Optional[scene.Scene]:
        return self.__cur_screen

    @cur_screen.setter
    def cur_screen(self, new_screen: scene.Scene) -> None:
        self.__cur_screen = new_screen

    def quit(self) -> None:
        sys.exit()

    def register_processor(
        self,
        event_type: int,
        func: Callable[
            [pygame.event.Event, Callable[..., None], Optional[dict[str, Any]]], bool
        ],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type in self.__processors:
            raise ValueError(f"A processor for event type {event_type} already exists.")
        self.__processors[event_type] = (func, options)

    def deregister_processor(
        self,
        event_type: int,
        func: Callable[[pygame.event.Event, Callable[..., None], dict[str, Any]], bool],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        warnings.warn(
            f"You are attempting to remove a processor for event type {event_type}. "
            "This is highly discouraged."
        )
        if event_type not in self.__processors:
            raise KeyError(f"No processor defined for event type {event_type}")
        if self.__processors[event_type][0] != func:
            raise ValueError(
                "The processor provided did not match the currently used processor. "
                f"Expected {self.__processors[event_type][0]}, received {func}"
            )
        if self.__processors[event_type][1] != options:
            raise ValueError(
                "The options argument provided did not match what was expected. "
                f"Expected {self.__processors[event_type][1]}, received {options}"
            )
        del self.__processors[event_type]

    def notify(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.quit()
        if self.__cur_screen is None:
            raise TypeError(
                "Current Screen has not been set. Please set this first before "
                "attempting to use event listeners"
            )
        listeners: list[dict[Callable[..., None], Optional[dict[str, Any]]]] = []
        if event.type in self.__cur_screen.listeners:
            listeners.append(self.__cur_screen.listeners[event.type])
        for layer in self.__cur_screen.elements:
            for e in layer:
                if event.type in e.listeners:
                    listeners.append(e.listeners[event.type])
        for listener in listeners:
            for func, options in listener.items():
                result: bool = self.__processors[event.type][0](event, func, options)
                if result and options is not None:
                    if "once" in options:
                        if options["once"]:
                            options["target"].deregister_listener(
                                event.type, func, options
                            )
