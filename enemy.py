import secrets
from typing import Optional

import pygame

import attack
import character
import entity
import sprite


class Enemy(character.Character):
    def __init__(
        self,
        surf: sprite.Sprite,
        name: str,
        mask: Optional[pygame.Rect] = None,
        health_regen_speed: float = 1.0,
        energy_regen_speed: float = 1.0,
        defense: int = 10,
        energy: float = 10.0,
        strength: int = 10,
        reward: float = 50.0,
    ):
        super().__init__(
            surf,
            name,
            health_regen_speed=health_regen_speed,
            energy_regen_speed=energy_regen_speed,
            defense=defense,
            energy=energy,
            strength=strength,
            mask=mask,
            reward=reward,
        )
        self.attacks: list[tuple[str, attack.Attack]] = [
            ("Charge", attack.Attack(0.5, 1))
        ]

    def choose_attack(self, target: entity.Entity) -> None:
        if self.health <= 0:
            return
        available_attacks: list[Optional[tuple[int, str, attack.Attack]]] = [
            (
                (i, attack_inst[0], attack_inst[1])
                if attack_inst[1].cost <= self.energy
                else None
            )
            for i, attack_inst in enumerate(self.attacks)
        ]
        attack_list_total_energy: int = sum(
            (val[2].cost if val is not None else 0 for val in available_attacks)
        )
        inverted_costs: list[int] = [
            attack_list_total_energy - val[2].cost if val is not None else 0
            for val in available_attacks
        ]
        inverted_total: int = sum(inverted_costs)
        if inverted_total <= 0:
            return
        num: int = secrets.randbelow(inverted_total)
        orig_num: int = int(str(num))
        for val in available_attacks:
            if val is not None:
                i, _, attack_inst = val
                if num < inverted_costs[i]:
                    self.attack(i, target)
                    break
                num -= inverted_costs[i]
        else:
            print(
                attack_list_total_energy, available_attacks, num, orig_num, self.attacks
            )
            raise RuntimeError("Something weird happened when choosing an enemy attack")
