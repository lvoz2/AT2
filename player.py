from typing import Any, Optional

import pygame

import attack
import character
import sprite

# import screen


class Player(character.Character):
    def __init__(
        self,
        design: sprite.Sprite,
        name: str,
        character_class: str,
        mask: Optional[pygame.Rect] = None,
        defense: int = 10,
        mana: int = 10,
        strength: int = 10,
        stamina: int = 10,
        stamina_regen_speed: int = 1,
        health_regen_speed: float = 1,
    ) -> None:
        super().__init__(
            design,
            name,
            health_regen_speed=health_regen_speed,
            defense=defense,
            mana=mana,
            strength=strength,
            mask=mask,
        )
        self.character_class = character_class
        self.stamina: int = stamina
        self.stamina_regen_speed = stamina_regen_speed
        self.max_stamina: int = stamina
        self.xp: int = 0
        self.inventory: list[Any] = []
        self.money: int = 0
        self.attr_pts: int = 0
        self.attr_pts_per_lvl: int = 3
        self.attacks: list[attack.Attack] = [attack.Attack(25, 0)]

    def assign_attr_pts(self, attr: str, pts: int) -> None:
        if attr in self.__dict__:
            setattr(self, attr, getattr(self, attr) + pts)
            self.attr_pts -= pts
        else:
            raise KeyError("Character attribute does not exist")

    def gain_xp(self, xp: int) -> None:
        self.xp += xp
        req_xp: int = self.calc_req_xp(self.lvl + 1)
        while self.xp >= req_xp and self.lvl < self.max_lvl:
            self.lvl += 1
            self.xp -= req_xp
            self.attr_pts += self.attr_pts_per_lvl
            # screen.show("Level Up", f"{self.name} is now level {self.level}")
            req_xp = self.calc_req_xp(self.lvl + 1)

    @staticmethod
    def calc_req_xp(lvl: int) -> int:
        return int((100 / 2) * lvl * (1 + lvl))

    def regen_stamina(self) -> None:
        if (self.stamina + self.stamina_regen_speed) <= self.max_stamina:
            self.stamina += self.stamina_regen_speed
        else:
            self.stamina = self.max_stamina

    def use_stamina(self, amount: int) -> bool:
        if (self.stamina - amount) >= 0:
            self.stamina -= amount
            return True
        return False
