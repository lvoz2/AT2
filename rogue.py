from typing import Any, Optional

import pygame

import display
import player


class Rogue(player.Player):
    def __init__(
        self,
        name: str,
        rect: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        mask: Optional[pygame.Rect] = None,
        scale: float = 1.0,
    ) -> None:
        window: display.Display = display.Display()
        super().__init__(
            window.get_asset(
                "assets/rogue.png", rect=rect, rect_options=rect_options, scale=scale
            ),
            name,
            "rogue",
            mask=mask,
            defense=15,
        )
