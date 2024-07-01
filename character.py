from typing import Any, Optional

import pygame

import attack
import dynentity
import entity
import sprite


class Character(dynentity.DynEntity):
    def __init__(
        self,
        design: sprite.Sprite,
        name: str,
        mask: Optional[pygame.Rect] = None,
        health_regen_speed: float = 5,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
    ) -> None:
        super().__init__(
            design,
            health=100,
            health_regen_speed=health_regen_speed,
            visible=True,
            mask=mask,
        )
        self.name = name
        self.lvl: int = 0
        self.skills: dict[str, Any] = {}
        self.attacks: list[attack.Attack] = []
        self.defense: int = defense
        self.mana: int = mana
        self.strength: int = strength
        self.max_lvl: int = 50

    def attack(self, category: int, target: entity.Entity, event_id: int) -> None:
        self.attacks[category].damage(target, event_id)
