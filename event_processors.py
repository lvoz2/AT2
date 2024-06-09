from typing import Any, Callable, Optional
import pygame
import events


def process_keydown(
    event: pygame.event.Event,
    func: Callable[[pygame.event.Event, dict[str, Any]], None],
    options: Optional[dict[str, Any]],
) -> None:
    if options is not None:
        if options["key"] == event.key and options["mods"] == event.mod:
            func(event, options)


def process_mouse_button_down(
    event: pygame.event.Event,
    func: Callable[[pygame.event.Event, dict[str, Any]], None],
    options: Optional[dict[str, Any]],
) -> None:
    if options is not None:
        if options["target"].rect.collidepoint(event.pos):
            func(event, options)


events_controller: events.Events = events.Events()
events_controller.register_processor(pygame.KEYDOWN, process_keydown)
events_controller.register_processor(pygame.MOUSEBUTTONDOWN, process_mouse_button_down)
