import pygame
import effect


class Entity:
    def __init__(self, surf: pygame.Surface, x: int, y: int, health: int = -1, health_regen_speed: float = 5, visible: bool = False, scale: int = 1) -> None:
        self.surf = surf.convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (int(self.surf.get_width() * scale), int(self.surf.get_height() * scale)))
        self.x = x
        self.y = y
        self.height = self.surf.get_height()
        self.width = self.surf.get_width()
        self.visible = visible
        self.health = health
        self.max_health = health
        self.health_regen_speed = health_regen_speed
        self.effects: dict[str, effect.Effect] = {}

    def get_opp_corner(self) -> list[int]:
        return [self.x + self.width, self.y + self.height]

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
            if ((0 - self.width) < self.x < window.get_width()) and ((0 - self.height) < self.y < window.get_height()):
                window.blit(self.surf, [self.x, self.y])
            else:
                self.visible = False
