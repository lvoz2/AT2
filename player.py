import asyncio
from typing import Any, Optional

import pygame

import character
import display
import enemy
import entity
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
        energy: float = 10.0,
        strength: int = 10,
        health_regen_speed: float = 1.0,
        energy_regen_speed: float = 1.0,
    ) -> None:
        super().__init__(
            design,
            name,
            health_regen_speed=health_regen_speed,
            energy_regen_speed=energy_regen_speed,
            defense=defense,
            energy=energy,
            strength=strength,
            mask=mask,
        )
        self.character_class = character_class
        self.__xp: float = 0
        # self.lvl: int = 0
        self.inventory: list[Any] = []
        self.money: int = 0
        self.attr_pts: int = 0
        self.attr_pts_per_lvl: int = 3

    # def __del__(self) -> None:
    #     pygame.event.post(pygame.event.Event(pygame.QUIT))
    #     print("deleting")
    #     super().__del__()

    async def enemy_attack_self(self, target: enemy.Enemy) -> None:
        await asyncio.sleep(0.5)
        target.choose_attack(self)

    def attack(self, category: int, target: entity.Entity) -> bool:
        try:
            res: bool = super().attack(category, target)
            if isinstance(target, enemy.Enemy):
                asyncio.run(
                    self.enemy_attack_self(
                        target,
                    )
                )
            if not res and isinstance(target, character.Character):
                self.gain_xp(target.reward)
            del target
            return res
        except ValueError as e:
            msg: str = str(e)
            if msg != "Inadequate energy to perform this action":
                raise e
            raise e

    def assign_attr_pts(self, attr: str, pts: int) -> None:
        if attr in self.__dict__:
            setattr(self, attr, getattr(self, attr) + pts)
            self.attr_pts -= pts
        else:
            raise KeyError("Character attribute does not exist")

    @property
    def xp(self) -> float:
        return self.__xp

    @xp.setter
    def xp(self, new_xp: float) -> None:
        if new_xp < self.__xp:
            raise ValueError("xp can only increase")
        self.__xp = new_xp
        window: display.Display = display.Display()
        stat_edit: pygame.event.Event = pygame.event.Event(
            window.events.event_types["stat_edit"], target=self, stat=("xp", self.__xp)
        )
        pygame.event.post(stat_edit)

    @xp.deleter
    def xp(self) -> None:
        del self.__xp

    def gain_xp(self, xp: float) -> None:
        self.xp += xp
        xp = self.xp
        req_xp: int = self.calc_req_xp(self.lvl + 1)
        while xp >= req_xp and self.lvl < self.max_lvl:
            self.lvl += 1
            xp -= req_xp
            self.attr_pts += self.attr_pts_per_lvl
            # screen.show("Level Up", f"{self.name} is now level {self.level}")
            req_xp = self.calc_req_xp(self.lvl + 1)

    @staticmethod
    def calc_req_xp(lvl: int) -> int:
        return int((100 / 2) * lvl * (1 + lvl))

    def regen_energy(self) -> None:
        if (self.energy + self.energy_regen_speed) <= self.max_energy:
            self.energy += self.energy_regen_speed
        else:
            self.energy = self.max_energy

    def damage(self, dmg: int) -> bool:
        super().damage(dmg)
        if not self.is_alive():
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return False
        return True
