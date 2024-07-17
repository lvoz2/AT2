from typing import Any, Optional

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
        self.attacks: list[tuple[str, attack.Attack]] = []
        self.defense: int = defense
        self.mana: int = mana
        self.strength: int = strength
        self.max_lvl: int = 50
        self.register_listener("dmg_event", self.go_to_game)

    def go_to_game(  # pylint: disable=unused-argument
        self,  # pylint: disable=unused-argument
        event: pygame.event.Event,  # pylint: disable=unused-argument
        options: dict[str, Any],  # pylint: disable=unused-argument
    ) -> None:  # pylint: disable=unused-argument
        if not self.is_alive():
            window: display.Display = display.Display()
            window.set_scene("game")

    def attack(self, category: int, target: entity.Entity, event_id: int) -> None:
        self.attacks[category][1].damage(self.strength, target, event_id)

    def damage(self, dmg: int, event_id: int) -> None:
        self.health -= min(dmg, self.health)
        dmg_event: pygame.event.Event = pygame.event.Event(event_id, target=self)
        pygame.event.post(dmg_event)
        if self.health == 0:
            window: display.Display = display.Display()
            for scene in window.scenes.values():
                for element_layer in scene.elements:
                    if self in element_layer:
                        element_layer.remove(self)
                        window.set_scene("game")
