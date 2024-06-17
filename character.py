from typing import Any, Optional

import pygame

import attack
import dynentity
import entity
import surf_rect


class Character(dynentity.DynEntity):
    def __init__(
        self,
        surf: surf_rect.Surf_Rect,
        name: str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        health_regen_speed: float = 5,
        scale: float = 1,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
    ) -> None:
        super().__init__(
            surf,
            health=100,
            health_regen_speed=health_regen_speed,
            visible=True,
            scale=scale,
            mask=mask,
            rect_options=rect_options,
            font_options=font_options,
        )
        self.name = name
        self.lvl: int = 0
        self.skills: dict[str, Any] = {}
        self.attacks: list[attack.Attack] = []
        self.defense: int = defense
        self.mana: int = mana
        self.strength: int = strength
        self.MAX_LVL: int = 50

    def attack(self, category: int, target: entity.Entity) -> None:
        self.attacks[category].damage(target)
