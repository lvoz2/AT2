from typing import Any, Optional

import pygame

import assets
import enemy


class Zombie(enemy.Enemy):
    def __init__(
        self,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        scale: int = 1,
    ):
        super().__init__(
            assets.get_asset("skeleton"),
            "Zombie",
            health_regen_speed=0.1,
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
            scale=scale,
        )
