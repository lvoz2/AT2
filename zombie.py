from typing import Any, Optional

import pygame

import enemy
import utils


class Zombie(enemy.Enemy):
    def __init__(
        self,
        rect: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        mask: Optional[pygame.Rect] = None,
    ):
        super().__init__(
            utils.get_asset(
                "assets/skeleton.png", rect=rect, rect_options=rect_options
            ),
            "Zombie",
            health_regen_speed=0.1,
            mask=mask,
        )
