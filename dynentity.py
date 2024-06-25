import math
from typing import Any, Optional

import pygame

import entity
import sprite


class DynEntity(entity.Entity):
    def __init__(
        self,
        design: sprite.Sprite,
        health: int,
        mask: Optional[pygame.Rect] = None,
        health_regen_speed: float = 5,
        visible: bool = False,
    ) -> None:
        super().__init__(
            design,
            mask=mask,
            health=health,
            health_regen_speed=health_regen_speed,
            visible=visible,
        )

    def move(self, direction: float, distance: float) -> None:
        """Move the dynamic entity.

        direction (float): The true bearing
        distance (int): The distance to move
        """
        while direction > 360.0:
            direction -= 360.0
        while direction < 0.0:
            direction += 360.0
        horizontal: float = 0.0
        vertical: float = 0.0
        if 0.0 <= direction <= 90.0:
            direction = math.radians(direction)
            horizontal = math.sin(direction) * distance
            vertical = -(math.cos(direction) * distance)
        elif 90.0 <= direction <= 180.0:
            direction = math.radians(180 - direction)
            horizontal = math.sin(direction) * distance
            vertical = math.cos(direction) * distance
        elif 180.0 <= direction <= 270.0:
            direction = math.radians(direction - 180)
            horizontal = -(math.sin(direction) * distance)
            vertical = math.cos(direction) * distance
        else:
            direction = math.radians(360 - direction)
            horizontal = -(math.sin(direction) * distance)
            vertical = -(math.cos(direction) * distance)
        self.design.rect.x += int(round(horizontal))
        self.design.rect.y += int(round(vertical))

    def get_distance(self, other: entity.Entity) -> float:
        if self.design.rect.colliderect(other.design.rect):
            return -1.0
        opp_corner: dict[str, list[int]] = {
            "self": self.get_opp_corner(),
            "other": other.get_opp_corner(),
        }
        linear_distances: list[float] = [
            abs(self.design.rect.y - opp_corner["other"][1]),
            abs(other.design.rect.x - opp_corner["self"][0]),
            abs(other.design.rect.y - opp_corner["self"][1]),
            abs(self.design.rect.x - opp_corner["other"][0]),
        ]
        horizontal: float = min(linear_distances[1], linear_distances[3])
        vertical: float = min(linear_distances[0], linear_distances[2])
        hypotenuse: float = math.sqrt(horizontal**2 + vertical**2)
        return hypotenuse

    def get_angle(self, other: entity.Entity) -> float:
        """Calculates the true bearing from self to other

        other: (entity.Entity)
        """
        horizontal: float = self.design.rect.center[0] - other.design.rect.center[0]
        vertical: float = self.design.rect.center[1] - other.design.rect.center[1]
        angle: float = math.atan2(vertical, horizontal)
        if angle < 0:
            return math.degrees(angle + math.pi + math.pi)
        return math.degrees(angle)

    def collide(self, other: entity.Entity, angle: bool = False) -> list[float]:
        """Returns the distance to another entity, and optionally, the bearing

        other (entity.Entity): The target entity
        angle (bool): Whether to calculate the true bearing, in degrees
        """
        if self.design.rect.colliderect(other.design.rect):
            return [0.0, 0.0]
        distance: float = self.get_distance(other)
        if angle:
            return [distance, self.get_angle(other)]
        return [distance]
