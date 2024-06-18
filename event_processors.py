import sys
from typing import Any, Callable, Optional

import pygame

import events


def process_keydown(
    event: pygame.event.Event,
    func: Callable[[pygame.event.Event, dict[str, Any]], None],
    options: Optional[dict[str, Any]],
) -> bool:
    if options is not None:
        if options["key"] == event.key and options["mods"] == event.mod:
            func(event, options)
            return True
    return False


def process_mouse_button_down(
    event: pygame.event.Event,
    func: Callable[[pygame.event.Event, dict[str, Any]], None],
    options: Optional[dict[str, Any]],
) -> bool:
    if options is not None:
        if options["target"].design.rect.collidepoint(event.pos):
            func(event, options)
            return True
    return False


def process_exit(  # pylint: disable=unused-argument
    event: pygame.event.Event,  # pylint: disable=unused-argument
    func: Callable[
        [pygame.event.Event, dict[str, Any]], None
    ],  # pylint: disable=unused-argument
    options: Optional[dict[str, Any]],  # pylint: disable=unused-argument
) -> bool:  # pylint: disable=unused-argument
    sys.exit()


def load() -> None:
    events_controller: events.Events = events.Events()
    events_controller.register_processor(pygame.QUIT, process_exit)
    events_controller.register_processor(pygame.KEYDOWN, process_keydown)
    events_controller.register_processor(
        pygame.MOUSEBUTTONDOWN, process_mouse_button_down
    )
