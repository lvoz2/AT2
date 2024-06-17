from typing import Any, Optional

import pygame

import character
import surf_rect


class Enemy(character.Character):
    def __init__(
        self,
        surf: surf_rect.Surf_Rect,
        name: str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        health_regen_speed: float = 1,
        scale: int = 1,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
    ):
        super().__init__(
            surf,
            name,
            health_regen_speed=health_regen_speed,
            scale=scale,
            defense=defense,
            mana=mana,
            strength=strength,
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
        )
