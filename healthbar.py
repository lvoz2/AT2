from typing import Any

import pygame

import element
import player
import sprite


class HealthBar(element.Element):
    def __init__(
        self, max_health: float, rect: pygame.Rect, rect_options: dict[str, Any]
    ) -> None:
        self.max_width = rect.width
        self.max_health = max_health
        design = sprite.Sprite(rect=rect, rect_options=rect_options)
        super().__init__(design, mask=pygame.Rect(0, 0, rect.width, rect.height))

    def update(self, new_health: int) -> None:
        if self.mask is not None:
            self.mask.width = int(self.max_width * (new_health / self.max_health))
