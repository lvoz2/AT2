from typing import Any, Optional

import pygame

import display
import player
import utils


class Warrior(player.Player):
    def __init__(
        self,
        name: str,
        rect: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        mask: Optional[pygame.Rect] = None,
        scale: float = 1.0,
    ) -> None:
        super().__init__(
            utils.get_asset(
                "assets/warrior.png", rect=rect, rect_options=rect_options, scale=scale
            ),
            name,
            "warrior",
            mask=mask,
            strength=15,
        )
