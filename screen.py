from typing import Any, Callable, Optional
import pygame
import entity


class Screen:
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.active_keys: dict[Any, Callable[[None], None]] = {}
        self.entities: list[list[Optional[entity.Entity]]] = [[None]]
        self.ui: list[list[None]] = [[None]]

    def register_key(self, key, action: Callable[[None], None]) -> None:
        pass

    def draw(self) -> None:
        pass
