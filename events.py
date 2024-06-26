import sys
import warnings
from typing import Any, Callable, Optional
from functools import lru_cache

import pygame

import scene
import singleton

# The way events will be handled is heavily influenced by JavaScript, especially
# addEventListener and removeEventListener. The interface for it should share its state
# across all instantiations, and so it is a Singleton. This file should implement the
# Observer design pattern, albeit with a slight difference: Events are first processed a
# little bit, so that, for example, a MouseDown listener is only fired when its target
# is actually clicked, instead of every MouseDown Event.


class Events(object, metaclass=singleton.Singleton):

    if not hasattr(__dict__, "created"):
        listener_maxsize: int = 300

    def __init__(self, listener_maxsize: int = 300) -> None:
        if not hasattr(self, "created"):
            self.listener_maxsize = listener_maxsize
            self.created: bool = True
            self.pressed_keys: list[int] = []
            self.__cur_screen: Optional[scene.Scene] = None
            self.__processors: dict[
                int,
                tuple[
                    Callable[
                        [
                            pygame.event.Event,
                            Callable[[pygame.event.Event, dict[str, Any]], None],
                            dict[str, Any],
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

    def default_processor(
        self,
        event: pygame.event.Event,
        func: Callable[[pygame.event.Event, dict[str, Any]], None],
        options: Optional[dict[str, Any]],
    ) -> bool:
        if options is not None:
            func(event, options)
            return True
        return False

    def register_processor(
        self,
        event_type: int,
        func: Callable[
            [pygame.event.Event, Callable[[pygame.event.Event, dict[str, Any]], None], Optional[dict[str, Any]]], bool
        ],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type in self.__processors:
            raise ValueError(f"A processor for event type {event_type} already exists.")
        self.__processors[event_type] = (func, options)

    def deregister_processor(
        self,
        event_type: int,
        func: Callable[[pygame.event.Event, Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]], bool],
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

    @lru_cache(maxsize=listener_maxsize)
    def __get_listeners(self, cur_scene: scene.Scene) -> dict[int, dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]]]:
        if cur_scene is None:
            raise TypeError(
                "Current Scene has not been set. Please set this first before "
                "attempting to use event listeners"
            )
        listeners: dict[int, dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]]] = cur_scene.listeners
        for layer in cur_scene.elements:
            for e in layer:
                for event_type, listeners_dict in e.listeners.items():
                    if listeners[event_type] is None:
                        listeners[event_type] = {}
                    for callback, options in listeners_dict.items():
                        listeners[event_type][callback] = options
        return listeners

    @property
    def active_listeners(self) -> dict[int, dict[Callable[[pygame.event.Event, dict[str, Any]], None], dict[str, Any]]]:
        return self.__get_listeners(self.__cur_screen)

    @active_listeners.deleter
    def active_listeners(self) -> None:
        self.__get_listeners.clear_cache()

    def notify(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.pressed_keys.append(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.remove(event.key)
        for func, options in self.active_listeners[event.type].items():
            result: bool = False
            if event.type in self.__processors:
                result = self.__processors[event.type][0](event, func, options)
            else:
                result = self.default_processor(event, func, options)
            if result and options is not None:
                if "once" in options:
                    if options["once"]:
                        options["target"].deregister_listener(
                            event.type, func, options
                        )
