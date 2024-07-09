from typing import Optional

import pygame

import display
import effect
import element
import sprite


class Entity(element.Element):
    def __init__(
        self,
        design: sprite.Sprite,
        mask: Optional[pygame.Rect] = None,
        health: float = -1.0,
        health_regen_speed: float = 5,
        visible: bool = False,
    ) -> None:
        super().__init__(
            design,
            mask=mask,
            visible=visible,
        )
        self.health = health
        self.max_health = health
        self.health_regen_speed = health_regen_speed
        self.effects: dict[str, effect.Effect] = {}

    def get_opp_corner(self) -> list[int]:
        return [
            self.design.x + self.design.width,
            self.design.y + self.design.height,
        ]

    def is_alive(self) -> bool:
        return self.health == 0

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

    def regen_health(self) -> None:
        if self.health > 0:
            if (self.health + self.health_regen_speed) <= self.max_health:
                self.health += self.health_regen_speed
            else:
                self.health = self.max_health
