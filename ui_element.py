from typing import Any, Optional

import pygame

import element
import sprite


class UI_Element(element.Element):
    def __init__(
        self,
        design: sprite.Sprite | str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        scale: float = 1.0,
    ) -> None:
        super().__init__(design, mask, rect_options, font_options, scale)
