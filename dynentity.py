from typing import Optional
import math
import pygame
from entity import Entity


class DynEntity(Entity):
    def __init__(self, surf: pygame.Surface, x: int, y: int, window: pygame.Surface, health: int, health_regen_speed: int = 5, visible: bool = False, scale: int = 1) -> None:
        super().__init__(surf, x, y, window, health, health_regen_speed, visible, scale)

    def move(self, dir: int, dist: int) -> None:
        """Move the dynamic entity.

        dir (int): A number representing the direction, with 0 being positive y, and 7 being positive y and negative x. It goes around clockwise
        dist (int): The number of pixels moved in 1d. For diagonal movements, this is not the hypotenuse
        """
        if dir in [1, 2, 3]:
            self.x += dist
        elif dir in [5, 6, 7]:
            self.x -= dist
        if dir in [0, 1, 7]:
            self.y += dist
        elif dir in [3, 4, 5]:
            self.y -= dist

    def find_eighth(self, other: Entity) -> list[Optional[int]]:
        dir: list[Optional[int]] = [None, None]
        opp_corner: dict[str, list[int]] = {"self": self.get_opp_corner(), "other": other.get_opp_corner()}
        if opp_corner["other"][0] < self.x:
            dir[0] = -1
        elif other.x > opp_corner["self"][0]:
            dir[0] = 1
        else:
            dir[0] = 0
        if opp_corner["other"][1] < self.y:
            dir[1] = -1
        elif other.y > opp_corner["self"][1]:
            dir[1] = 1
        else:
            dir[1] = 0
        if None in dir:
            raise ValueError("Could not determine which eighth the other entity was located in relative to self")
        return dir

    def get_dist(self, dir: int, other: Entity, angle: bool) -> Optional[float]:
        opp_corner: dict[str, list[int]] = {"self": self.get_opp_corner(), "other": other.get_opp_corner()}
        angle_val: Optional[float] = None
        lin_dists: list[float] = [
            self.y - opp_corner["other"][1],
            other.x - opp_corner["self"][0],
            other.y - opp_corner["self"][1],
            self.x - opp_corner["other"][0]
        ]
        if dir == [0, -1]:
            if angle:
                angle_val = 0.0
            dist = lin_dists[0]
        elif dir == [1, -1]:
            if angle:
                angle_val = math.degrees(math.tan(lin_dists[1]/lin_dists[0]))
            dist = math.sqrt(math.pow(lin_dists[0], 2) + math.pow(lin_dists[1], 2))
        elif dir == [1, 0]:
            if angle:
                angle_val = 90.0
            dist = lin_dists[1]
        elif dir == [1, 1]:
            if angle:
                angle_val = math.degrees(math.tan(lin_dists[2]/lin_dists[1])) + 90.0
            dist = math.sqrt(math.pow(lin_dists[1], 2) + math.pow(lin_dists[2], 2))
        elif dir == [0, 1]:
            if angle:
                angle_val = 180.0
            dist = lin_dists[2]
        elif dir == [-1, 1]:
            if angle:
                angle_val = math.degrees(math.tan(lin_dists[3]/lin_dists[2])) + 180.0
            dist = math.sqrt(math.pow(lin_dists[2], 2) + math.pow(lin_dists[3], 2))
        elif dir == [-1, 0]:
            if angle:
                angle_val = 270.0
            dist = lin_dists[3]
        elif dir == [-1, -1]:
            if angle:
                angle_val = math.degrees(math.tan(lin_dists[0]/lin_dists[3])) + 270.0
            dist = math.sqrt(math.pow(lin_dists[3], 2) + math.pow(lin_dists[0], 2))
        if dist is None:
            raise ValueError("Could not determine distance properly, which may be due to a failure to calculate distance or because other entity overlapped self but not detected")
        if angle_val is None and angle:
            raise ValueError("Could not determine angle properly, which may be due to a failure to calculate angle or because other entity overlapped self but not detected")
        if angle:
            return [dist, angle_val]
        return [dist]

    def collide(self, other: Entity, angle: bool = False) -> list[Optional[float]]:
        """Calculates the distance to another entity

        other (Entity): The target entity
        angle (bool): Whether to calculate the angle, in degrees. Defaults to False
        """
        dir: list[Optional[int]] = self.find_eighth(other)
        if dir == [0, 0] and not angle:
            return [0.0]
        return self.get_dist(dir, other)
