from typing import Any

import pygame

from dynentity import DynEntity
from entity import Entity
from attack import Attack


class Character(DynEntity):
	def __init__(self, surf: pygame.Surface, x: int, y: int, window: pygame.Surface, name: str, health_regen_speed: int = 5, scale: int = 1, defense: int = 10, mana: int = 10, strength: int = 10) -> None:
	super().__init__(surf, x, y, window, 100, health_regen_speed, True, scale)
	self.name = name
	self.lvl: int = 0
	self.skills: dict[str, Any] = {}
	self.attacks: list[Attack] = []
	self.defense: int = defense
	self.mana: int = mana
	self.strength: int = strength
	self.max_lvl: int = 50

	def attack(self, type: int, target: Entity) -> None:
	self.attacks[type].damage(target)
