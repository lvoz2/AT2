from typing import Any, Callable
import pygame
import entity


class Screen:
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.active_keys: dict[Any, Callable[[], None]] = {}
        self.entities: list[list[entity.Entity]] = [[]]
        self.ui: list[list[entity.Entity]] = [[]]

    def register_key(self, key, action: Callable[[None], None]) -> None:
        pass

    def draw(self) -> None:
        pass
