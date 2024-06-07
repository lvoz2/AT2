from typing import Optional
import math
import pygame
import entity


class DynEntity(entity.Entity):
    def __init__(
        self,
        surf: pygame.Surface,
        x: int,
        y: int,
        health: int,
        health_regen_speed: float = 5,
        visible: bool = False,
        scale: int = 1,
    ) -> None:
        super().__init__(surf, x, y, health, health_regen_speed, visible, scale)

    def move(self, direction: int, distance: int) -> None:
        """Move the dynamic entity.

        direction (int): A number representing the direction
        distance (int): The number of pixels moved laterally
        """
        if direction in [1, 2, 3]:
            self.x += distance
        elif direction in [5, 6, 7]:
            self.x -= distance
        if direction in [0, 1, 7]:
            self.y += distance
        elif direction in [3, 4, 5]:
            self.y -= distance

    def find_eighth(self, other: entity.Entity) -> list[Optional[int]]:
        direction: list[Optional[int]] = [None, None]
        opp_corner: dict[str, list[int]] = {
            "self": self.get_opp_corner(),
            "other": other.get_opp_corner(),
        }
        if opp_corner["other"][0] < self.x:
            direction[0] = -1
        elif other.x > opp_corner["self"][0]:
            direction[0] = 1
        else:
            direction[0] = 0
        if opp_corner["other"][1] < self.y:
            direction[1] = -1
        elif other.y > opp_corner["self"][1]:
            direction[1] = 1
        else:
            direction[1] = 0
        if None in direction:
            raise ValueError(
                "Could not determine which eighth the other entity was located"
                " in relative to self"
            )
        return direction

    def get_dist(
        self, direction: list[Optional[int]], other: entity.Entity, angle: bool
    ) -> list[Optional[float]]:
        opp_corner: dict[str, list[int]] = {
            "self": self.get_opp_corner(),
            "other": other.get_opp_corner(),
        }
        angle_val: Optional[float] = None
        lin_dists: list[float] = [
            self.y - opp_corner["other"][1],
            other.x - opp_corner["self"][0],
            other.y - opp_corner["self"][1],
            self.x - opp_corner["other"][0],
        ]
        rad: Optional[float] = None
        a_squared: Optional[float] = None
        b_squared: Optional[float] = None
        dist: Optional[float] = None
        if direction == [0, -1]:
            if angle:
                angle_val = 0.0
            dist = lin_dists[0]
        elif direction == [1, -1]:
            if angle:
                rad = math.tan(lin_dists[1] / lin_dists[0])
                angle_val = math.degrees(rad)
            a_squared = math.pow(lin_dists[0], 2)
            b_squared = math.pow(lin_dists[1], 2)
            dist = math.sqrt(a_squared + b_squared)
        elif direction == [1, 0]:
            if angle:
                angle_val = 90.0
            dist = lin_dists[1]
        elif direction == [1, 1]:
            if angle:
                rad = math.tan(lin_dists[2] / lin_dists[1])
                angle_val = math.degrees(rad) + 90.0
            a_squared = math.pow(lin_dists[1], 2)
            b_squared = math.pow(lin_dists[2], 2)
            dist = math.sqrt(a_squared + b_squared)
        elif direction == [0, 1]:
            if angle:
                angle_val = 180.0
            dist = lin_dists[2]
        elif direction == [-1, 1]:
            if angle:
                rad = math.tan(lin_dists[3] / lin_dists[2])
                angle_val = math.degrees(rad) + 180.0
            a_squared = math.pow(lin_dists[2], 2)
            b_squared = math.pow(lin_dists[3], 2)
            dist = math.sqrt(a_squared + b_squared)
        elif direction == [-1, 0]:
            if angle:
                angle_val = 270.0
            dist = lin_dists[3]
        elif direction == [-1, -1]:
            if angle:
                rad = math.tan(lin_dists[0] / lin_dists[3])
                angle_val = math.degrees(rad) + 270.0
            a_squared = math.pow(lin_dists[3], 2)
            b_squared = math.pow(lin_dists[0], 2)
            dist = math.sqrt(a_squared + b_squared)
        if dist is None:
            raise ValueError(
                "Could not determine distance properly, which \
            may be due to a failure to calculate distance or because other \
            entity overlapped self but not detected"
            )
        if angle_val is None and angle:
            raise ValueError(
                "Could not determine angle properly, which may \
            be due to a failure to calculate angle or because other entity \
            overlapped self but not detected"
            )
        if angle:
            return [dist, angle_val]
        return [dist]

    def collide(
        self, other: entity.Entity, angle: bool = False
    ) -> list[Optional[float]]:
        """Calculates the distance to another entity

        other (entity.Entity): The target entity
        angle (bool): Whether to calculate the angle, in degrees
        """
        direction: list[Optional[int]] = self.find_eighth(other)
        if direction == [0, 0] and not angle:
            return [0.0]
        return self.get_dist(direction, other, angle)
