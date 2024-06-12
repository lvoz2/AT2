from typing import Any, Callable, Optional
import pygame
import element
import entity
import surf_rect
import ui_element


class Screen(element.Element):
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.listeners: dict[
            int, dict[Callable[..., None], Optional[dict[str, Any]]]
        ] = {}
        self.elements: list[list[entity.Entity | ui_element.UI_Element]] = [[]]
