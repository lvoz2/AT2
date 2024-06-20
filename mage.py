from typing import Any, Optional

import pygame

import display
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
        window: display.Display = display.Display()
        super().__init__(
            window.get_asset("assets/mage.png"),
            name,
            "mage",
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
            scale=scale,
            mana=15,
        )
