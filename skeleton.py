from typing import Any, Optional

import pygame

import attack
import enemy
import utils


class Skeleton(enemy.Enemy):
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
            "Skeleton",
            health_regen_speed=0.1,
            mask=mask,
            reward=50.0,
        )
        self.attacks: list[tuple[str, attack.Attack]] = [
            ("Throw", attack.Attack(2.5, 2)),
            ("Slam", attack.Attack(4, 4)),
            ("Skelton's Rage", attack.Attack(6, 8)),
        ]
