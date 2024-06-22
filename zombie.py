from typing import Any, Optional

import pygame

import display
import enemy


class Zombie(enemy.Enemy):
    def __init__(
        self,
        rect_options: Optional[dict[str, Any]] = None,
        mask: Optional[pygame.Rect] = None,
    ):
        window: display.Display = display.Display()
        super().__init__(
            window.get_asset("assets/skeleton.png", rect_options),
            "Zombie",
            health_regen_speed=0.1,
            mask=mask,
        )
