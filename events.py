import sys
import warnings
from typing import Any, Callable, Optional

import pygame

import scene
import utils

# The way events will be handled is heavily influenced by JavaScript, especially
# addEventListener and removeEventListener. The interface for it should share its state
# across all instantiations, and so it is a Singleton. This file should implement the
# Observer design pattern, albeit with a slight difference: Events are first processed a
# little bit, so that, for example, a MouseDown listener is only fired when its target
# is actually clicked, instead of every MouseDown Event.


class Events(metaclass=utils.Singleton):
    def __init__(self) -> None:
        if not hasattr(self, "created"):
            self.created: bool = True
            self.pressed_keys: list[int] = []
            self.__cur_scene: Optional[scene.Scene] = None
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
            # The following dict of event types are the types reserved by SDL2.
            # I had to find where they were set in SDL2's source code to use them here
            # Not all (I don't think all) are actually mentioned in the pygame docs,
            # and if more event codes are required than the 32669 pygame.USEREVENT codes
            # available, this dict can be used to find what's free
            self.event_types: dict[str, int] = {
                "first_event": 0x0,
                "quit": pygame.QUIT,
                "app_terminating": pygame.APP_TERMINATING,
                "app_low_memory": pygame.APP_LOWMEMORY,
                "app_will_enter_background": pygame.APP_WILLENTERBACKGROUND,
                "app_did_enter_background": pygame.APP_DIDENTERBACKGROUND,
                "app_will_enter_foreground": pygame.APP_WILLENTERFOREGROUND,
                "app_did_enter_foreground": pygame.APP_DIDENTERFOREGROUND,
                "locale_changed": pygame.LOCALECHANGED,
                "display_event": 0x150,
                "window_event": 0x200,
                "sys_wm_event": pygame.SYSWMEVENT,  # Not in docs
                "key_down": pygame.KEYDOWN,
                "key_up": pygame.KEYUP,
                "text_editing": pygame.TEXTEDITING,
                "text_input": pygame.TEXTINPUT,
                "key_map_changed": pygame.KEYMAPCHANGED,
                "text_editing_ext": 0x305,
                "mouse_motion": pygame.MOUSEMOTION,
                "mouse_button_down": pygame.MOUSEBUTTONDOWN,
                "mouse_button_up": pygame.MOUSEBUTTONUP,
                "mouse_wheel": pygame.MOUSEWHEEL,
                "joy_axis_motion": pygame.JOYAXISMOTION,
            }

    @property
    def cur_scene(self) -> Optional[scene.Scene]:
        return self.__cur_scene

    @cur_scene.setter
    def cur_scene(self, new_scene: scene.Scene) -> None:
        self.__cur_scene = new_scene

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
            [
                pygame.event.Event,
                Callable[[pygame.event.Event, dict[str, Any]], None],
                Optional[dict[str, Any]],
            ],
            bool,
        ],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type in self.__processors:
            raise ValueError(f"A processor for event type {event_type} already exists.")
        self.__processors[event_type] = (func, options)

    def deregister_processor(
        self,
        event_type: int,
        func: Callable[
            [
                pygame.event.Event,
                Callable[[pygame.event.Event, dict[str, Any]], None],
                dict[str, Any],
            ],
            bool,
        ],
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

    def notify(
        self,
        event: pygame.event.Event,
        listeners: Optional[
            dict[
                int,
                dict[
                    Callable[[pygame.event.Event, dict[str, Any]], None],
                    list[dict[str, Any]],
                ],
            ]
        ],
    ) -> None:
        if event.type == pygame.QUIT:
            self.quit()
        elif event.type == pygame.KEYDOWN:
            self.pressed_keys.append(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.remove(event.key)
        if listeners is None:
            return
        if event.type not in listeners:
            return
        for func, options_list in listeners[event.type].items():
            for options in options_list:
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
