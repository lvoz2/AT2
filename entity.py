from typing import Any, Optional

import pygame

import effect
import element
import sprite


class Entity(element.Element):
    def __init__(
        self,
        design: sprite.Sprite,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        health: float = -1.0,
        health_regen_speed: float = 5,
        visible: bool = False,
        scale: float = 1,
    ) -> None:
        super().__init__(
            design,
            rect_options=rect_options,
            mask=mask,
            font_options=font_options,
            scale=scale,
            visible=visible,
        )
        self.health = health
        self.max_health = health
        self.health_regen_speed = health_regen_speed
        self.effects: dict[str, effect.Effect] = {}

    def get_opp_corner(self) -> list[int]:
        return [self.x + self.design.rect.width, self.y + self.design.rect.height]

    def is_alive(self) -> bool:
        return self.health == 0

    def damage(self, dmg: int) -> None:
        if dmg >= self.health:
            self.health = 0
        else:
            self.health -= dmg

    def regen_health(self) -> None:
        if self.health > 0:
            if (self.health + self.health_regen_speed) <= self.max_health:
                self.health += self.health_regen_speed
            else:
                self.health = self.max_health

    def draw(self, window: pygame.Surface) -> None:
        if self.visible:
            if ((0 - self.design.rect.width) < self.x < window.get_width()) and (
                (0 - self.design.rect.height) < self.y < window.get_height()
            ):
                self.design.rect = window.blit(self.design.surf, [self.x, self.y])
            else:
                self.visible = False
