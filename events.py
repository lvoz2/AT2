import copy
import sys
import types
import warnings
from typing import TYPE_CHECKING, Any, Callable, Optional

import pygame

import utils

if TYPE_CHECKING:
    import scene

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
            self.__pressed_keys: dict[str, list[int]] = {
                "keys": [],
                "mods": [],
                "unicode": [],
                "scancode": [],
            }
            self.__repeat: bool = False
            self.__repeat_initial_delay: int = 0
            self.__repeat_interval: int = 0
            self.__cur_scene: Optional["scene.Scene"] = None
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
            # available, this dict can be used to find what's free. Also available to
            # do lookups
            self.__event_types: dict[str, int] = {
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
                "joy_ball_motion": pygame.JOYBALLMOTION,
                "joy_hat_motion": pygame.JOYHATMOTION,
                "joy_button_down": pygame.JOYBUTTONDOWN,
                "joy_button_up": pygame.JOYBUTTONUP,
                "joy_device_added": pygame.JOYDEVICEADDED,
                "joy_device_removed": pygame.JOYDEVICEREMOVED,
                "joy_battery_updated": 0x607,
                "controller_axis_motion": pygame.CONTROLLERAXISMOTION,
                "controller_button_down": pygame.CONTROLLERBUTTONDOWN,
                "controller_button_up": pygame.CONTROLLERBUTTONUP,
                "controller_device_added": pygame.CONTROLLERDEVICEADDED,
                "controller_device_removed": pygame.CONTROLLERDEVICEREMOVED,
                "controller_device_remapped": pygame.CONTROLLERDEVICEREMAPPED,
                "controller_touch_pad_down": pygame.CONTROLLERTOUCHPADDOWN,
                "controller_touch_pad_motion": pygame.CONTROLLERTOUCHPADMOTION,
                "controller_touch_pad_up": pygame.CONTROLLERTOUCHPADUP,
                "controller_sensor_update": pygame.CONTROLLERSENSORUPDATE,
                "controller_update_complete": 0x660,  # Reserved for SDL3, do not use
                "controller_steam_handle_updated": 0x661,
                "finger_down": pygame.FINGERDOWN,
                "finger_up": pygame.FINGERUP,
                "finger_motion": pygame.FINGERMOTION,
                "dollar_gesture": 0x800,
                "dollar_record": 0x801,
                "multi_gesture": pygame.MULTIGESTURE,
                "clipboard_update": pygame.CLIPBOARDUPDATE,
                "drop_file": pygame.DROPFILE,
                "drop_text": pygame.DROPTEXT,
                "drop_begin": pygame.DROPBEGIN,
                "drop_complete": pygame.DROPCOMPLETE,
                "audio_device_added": pygame.AUDIODEVICEADDED,
                "audio_device_removed": pygame.AUDIODEVICEREMOVED,
                "sensor_update": 0x1200,
                "render_targets_reset": pygame.RENDER_TARGETS_RESET,
                "render_device_reset": pygame.RENDER_DEVICE_RESET,
                "poll_sentinel": 0x7F00,
            }
            self.__reversed_event_types: dict[int, str] = {
                event_id: event_name
                for event_name, event_id in self.__event_types.items()
            }
            self.__pygame_evts = types.MappingProxyType(copy.deepcopy(self.event_types))
            self.__reversed_pygame_evts = types.MappingProxyType(
                copy.deepcopy(self.reversed_event_types)
            )
            self.event_types["key_press"] = pygame.event.custom_type()
            self.event_types["dmg_event"] = pygame.event.custom_type()
            self.event_types["switch_scene"] = pygame.event.custom_type()

            def __process_key_up_or_down(
                event: pygame.event.Event,
                func: Callable[[pygame.event.Event, dict[str, Any]], None],
                options: Optional[dict[str, Any]],
            ) -> bool:
                if options is not None:
                    if options["key"] == event.key and options["mods"] == event.mod:
                        func(event, options)
                        return True
                return False

            def __process_mouse_button_down(
                event: pygame.event.Event,
                func: Callable[[pygame.event.Event, dict[str, Any]], None],
                options: Optional[dict[str, Any]],
            ) -> bool:
                if options is not None:
                    if options["target"].design.rect.collidepoint(event.pos):
                        func(event, options)
                        return True
                return False

            def __process_exit(  # pylint: disable=unused-argument
                event: pygame.event.Event,  # pylint: disable=unused-argument
                func: Callable[
                    [pygame.event.Event, dict[str, Any]], None
                ],  # pylint: disable=unused-argument
                options: Optional[dict[str, Any]],  # pylint: disable=unused-argument
            ) -> bool:  # pylint: disable=unused-argument
                sys.exit()

            def __process_dmg(
                event: pygame.event.Event,
                func: Callable[[pygame.event.Event, dict[str, Any]], None],
                options: Optional[dict[str, Any]],
            ) -> bool:
                if options is not None:
                    if options["target"] == event.target:
                        func(event, options)
                        return True
                return False

            def __process_key_press(
                event: pygame.event.Event,
                func: Callable[[pygame.event.Event, dict[str, Any]], None],
                options: Optional[dict[str, Any]],
            ) -> bool:
                if options is not None:
                    keys_in: int = 0
                    mods_in: int = 0
                    for key in options["key"]:
                        keys_in += int(key in event.key)
                        if keys_in > 0:
                            break
                    for mod in options["mods"]:
                        mods_in += int(mod in event.mod)
                        if mods_in > 0:
                            break
                    if keys_in > 0 and mods_in > 0:
                        func(event, options)
                        return True
                return False

            self.register_processor("quit", __process_exit)
            self.register_processor("key_down", __process_key_up_or_down)
            self.register_processor("key_up", __process_key_up_or_down)
            self.register_processor("mouse_button_down", __process_mouse_button_down)
            self.register_processor("dmg_event", __process_dmg)
            self.register_processor("key_press", __process_key_press)

    @property
    def event_types(self) -> dict[str, int]:
        return self.__event_types

    @event_types.setter
    def event_types(self, new_event_types: dict[str, int]) -> None:
        self.__event_types = new_event_types
        self.__reversed_event_types = {
            event_id: event_name for event_name, event_id in new_event_types.items()
        }

    @property
    def reversed_event_types(self) -> dict[int, str]:
        return self.__reversed_event_types

    @reversed_event_types.setter
    def reversed_event_types(self, new_reversed_event_types: dict[int, str]) -> None:
        self.__reversed_event_types = new_reversed_event_types
        self.__event_types = {
            event_id: event_name
            for event_name, event_id in new_reversed_event_types.items()
        }

    @property
    def pygame_evts(self) -> types.MappingProxyType[str, int]:
        return self.__pygame_evts

    @property
    def reversed_pygame_evts(self) -> types.MappingProxyType[int, str]:
        return self.__reversed_pygame_evts

    def get_event_id(self, event_name: str) -> int:
        if event_name not in self.event_types:
            raise ValueError(f"No event with name {event_name} is in event_types")
        return self.event_types[event_name]

    def get_event_name(self, event_id: int) -> str:
        if event_id not in self.reversed_event_types:
            raise ValueError(f"No event with id {event_id} in event_types")
        return self.reversed_event_types[event_id]

    @property
    def cur_scene(self) -> Optional["scene.Scene"]:
        return self.__cur_scene

    @cur_scene.setter
    def cur_scene(self, new_scene: "scene.Scene") -> None:
        self.__cur_scene = new_scene

    def start_repeat(self) -> None:
        if self.__repeat_initial_delay == self.__repeat_interval == 0:
            raise ValueError(
                "A delay and/or repeat must be specified to repeat keypresses"
            )
        self.__repeat = True

    def set_key_repeat(self, initial_delay: int = 0, interval: int = 0) -> None:
        if initial_delay == interval == 0:
            return
        if initial_delay == 0:
            initial_delay = interval
        elif interval == 0:
            interval = initial_delay
        self.__repeat_initial_delay = initial_delay
        self.__repeat_interval = interval
        self.start_repeat()

    def create_key_press_event(self, full_delta: int) -> int:
        if (
            len(self.__pressed_keys["keys"])
            == len(self.__pressed_keys["mods"])
            == len(self.__pressed_keys["unicode"])
            == len(self.__pressed_keys["scancode"])
            == 0
        ):
            return 0
        evt: pygame.event.Event = pygame.event.Event(
            self.event_types["key_press"],
            key=self.__pressed_keys["keys"],
            mod=self.__pressed_keys["mods"],
            unicode=self.__pressed_keys["unicode"],
            scancode=self.__pressed_keys["scancode"],
        )
        if self.__repeat:
            loops: int = full_delta // self.__repeat_interval
            pygame.time.set_timer(evt, self.__repeat_interval, loops=loops)
            return full_delta % self.__repeat_interval
        if full_delta >= self.__repeat_initial_delay:
            pygame.time.set_timer(evt, self.__repeat_initial_delay, loops=1)
            return int(full_delta - self.__repeat_initial_delay)
        return full_delta

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
        event_type: int | str,
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
        if (isinstance(event_type, str) and event_type not in self.event_types) or (
            isinstance(event_type, int) and event_type not in self.reversed_event_types
        ):
            if isinstance(event_type, str):
                raise ValueError(
                    f"No event type exists as of yet with string {event_type}"
                )
            raise ValueError(f"No event type exists as of yet with int {event_type}")
        if isinstance(event_type, str):
            event_type = self.get_event_id(event_type)
        if event_type in self.__processors:
            raise ValueError(f"A processor for event type {event_type} already exists.")
        self.__processors[event_type] = (func, options)

    def deregister_processor(
        self,
        event_type: int | str,
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
        if (isinstance(event_type, str) and event_type not in self.event_types) or (
            isinstance(event_type, int) and event_type not in self.reversed_event_types
        ):
            if isinstance(event_type, str):
                raise ValueError(
                    f"No event type exists as of yet with string {event_type}"
                )
            raise ValueError(f"No event type exists as of yet with int {event_type}")
        if isinstance(event_type, str):
            event_type = self.get_event_id(event_type)
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
            self.__pressed_keys["keys"].append(event.key)
            self.__pressed_keys["mods"].append(event.mod)
            self.__pressed_keys["unicode"].append(event.unicode)
            self.__pressed_keys["scancode"].append(event.scancode)
        elif event.type == pygame.KEYUP:
            self.__pressed_keys["keys"].remove(event.key)
            self.__pressed_keys["mods"].remove(event.mod)
            self.__pressed_keys["unicode"].remove(event.unicode)
            self.__pressed_keys["scancode"].remove(event.scancode)
            if (
                len(self.__pressed_keys["keys"])
                == len(self.__pressed_keys["mods"])
                == len(self.__pressed_keys["unicode"])
                == len(self.__pressed_keys["scancode"])
                == 0
            ):
                self.__repeat = False
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
