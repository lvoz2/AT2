import functools
import gc

# import sys
from typing import Any, Callable, Optional

import pygame

import attack
import display
import dynentity
import entity
import sprite


class Character(dynentity.DynEntity):
    def __init__(
        self,
        design: sprite.Sprite,
        name: str,
        mask: Optional[pygame.Rect] = None,
        health_regen_speed: float = 5.0,
        energy_regen_speed: float = 1.0,
        defense: int = 10,
        energy: float = 10.0,
        strength: int = 10,
        reward: float = 50.0,
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
        self.attacks: list[tuple[str, attack.Attack]] = []
        self.defense: int = defense
        self.__energy: float = energy
        self.energy_regen_speed: float = energy_regen_speed
        self.max_energy: float = energy
        self.strength: int = strength
        self.max_lvl: int = 50
        self.register_listener("stat_edit", self.go_to_game)
        self.reward = reward

    def go_to_game(  # pylint: disable=unused-argument
        self,  # pylint: disable=unused-argument
        event: pygame.event.Event,  # pylint: disable=unused-argument
        options: dict[str, Any],  # pylint: disable=unused-argument
    ) -> None:  # pylint: disable=unused-argument
        if not self.is_alive():
            window: display.Display = display.Display()
            window.set_scene("game")
        del self

    def attack(self, category: int, target: entity.Entity) -> bool:
        if self.attacks[category][1].cost <= self.energy:
            res: bool = self.attacks[category][1].damage(self.strength, target)
            del target
            gc.collect()
            self.energy -= self.attacks[category][1].cost
            return res
        raise ValueError("Inadequate energy to perform this action")

    def damage(self, dmg: int) -> bool:
        self.health -= min(dmg, self.health)
        if self.health == 0:
            window: display.Display = display.Display()
            evt: pygame.event.Event = pygame.event.Event(
                window.events.event_types["death_event"], target=self
            )
            pygame.event.post(evt)
            for scene in window.scenes.values():
                listeners: list[
                    tuple[
                        int,
                        Callable[
                            [pygame.event.Event, dict[str, Any]],
                            Optional[functools.partial[None]],
                        ],
                    ]
                ] = []
                for scene_event_id in scene.listeners.keys():
                    for listener, options in scene.listeners[scene_event_id].items():
                        if self in options.values():
                            listeners.append((scene_event_id, listener))
                for scene_event_id, listener in listeners:
                    scene.deregister_listener(scene_event_id, listener)
                for element_layer in scene.elements:
                    if self in element_layer:
                        element_layer.remove(self)
                        # del self.listeners
                        # del self.attacks
                        # del self.design
                        self.deregister_listener("stat_edit", self.go_to_game)
                        gc.collect()
                        # print("gc", gc.garbage)
                        # print("refcount", sys.getrefcount(self) - 1)
                        # print("gc_ref", gc.get_referrers(self)[1:])
                        # print(self)
                        window.set_scene("game")
            return False
        return True

    @property
    def energy(self) -> float:
        return self.__energy

    @energy.setter
    def energy(self, new_energy: float) -> None:
        self.__energy = new_energy
        window: display.Display = display.Display()
        stat_edit: pygame.event.Event = pygame.event.Event(
            window.events.event_types["stat_edit"],
            target=self,
            stat=("energy", self.__energy),
        )
        pygame.event.post(stat_edit)

    @energy.deleter
    def energy(self) -> None:
        del self.__energy
