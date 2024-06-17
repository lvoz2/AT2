from typing import Any, Optional

import pygame

import assets
import player


class Rogue(player.Player):
    def __init__(
        self,
        name: str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        scale: float = 1,
    ):
        super().__init__(
            assets.get_asset("rogue"),
            name,
            "rogue",
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
            scale=scale,
            defense=15,
        )
        # Additional attributes and methods specific to the Rogue class
