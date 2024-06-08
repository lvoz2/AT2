from typing import Any

import pygame

import dynentity
import entity
import attack
import surf_rect


class Character(dynentity.DynEntity):
    def __init__(
        self,
        surf: surf_rect.Surf_Rect,
        x: int,
        y: int,
        name: str,
        health_regen_speed: float = 5,
        scale: float = 1,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
    ) -> None:
        super().__init__(surf, x, y, 100, health_regen_speed, True, scale)
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
