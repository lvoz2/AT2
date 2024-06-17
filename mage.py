from typing import Any, Optional

import pygame

import assets
import player


class Mage(player.Player):
    def __init__(
        self,
        name: str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        scale: float = 1,
    ) -> None:
        super().__init__(
            assets.get_asset("mage"),
            name,
            "mage",
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
            scale=scale,
            mana=15,
        )
