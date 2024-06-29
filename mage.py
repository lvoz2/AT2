from typing import Any, Optional

import pygame

import player
import utils


class Mage(player.Player):
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
                "assets/mage.png", rect=rect, rect_options=rect_options, scale=scale
            ),
            name,
            "mage",
            mask=mask,
            mana=15,
        )
