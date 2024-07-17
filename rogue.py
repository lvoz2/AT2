from typing import Any, Optional

import pygame

import attack
import player
import utils


class Rogue(player.Player):
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
                "assets/rogue.png", rect=rect, rect_options=rect_options, scale=scale
            ),
            name,
            "rogue",
            mask=mask,
            defense=15,
        )
        self.attacks: list[tuple[str, attack.Attack]] = [
            ("Charge", attack.Attack(2.5, 0))
        ]
