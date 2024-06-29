from typing import Optional

import pygame

import attack
import character
import sprite


class Enemy(character.Character):
    def __init__(
        self,
        surf: sprite.Sprite,
        name: str,
        mask: Optional[pygame.Rect] = None,
        health_regen_speed: float = 1,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
    ):
        super().__init__(
            surf,
            name,
            health_regen_speed=health_regen_speed,
            defense=defense,
            mana=mana,
            strength=strength,
            mask=mask,
        )
        self.attacks: list[attack.Attack] = [attack.Attack(5, 0)]
