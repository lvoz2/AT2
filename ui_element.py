from typing import Any, Optional

import pygame

import element
import sprite


class UI_Element(element.Element):
    def __init__(
        self,
        design: sprite.Sprite,
        mask: Optional[pygame.Rect] = None,
    ) -> None:
        super().__init__(design, mask)
