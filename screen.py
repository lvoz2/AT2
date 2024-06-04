from typing import Callable
import pygame
import entity
import ui_element


class Screen:
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.active_keys: dict[dict[str, int], tuple[str, Callable[[], None]]] = {}
        self.clickables: dict[pygame.Surface, tuple[str, Callable[[], None]]] = {}
        self.entities: list[list[entity.Entity]] = [[]]
        self.ui: list[list[ui_element.UI_Element]] = [[]]

    def register_key(self, name: str, key: int, mods: int, action: Callable[[], None]) -> None:
        combo: dict[str, int] = {"key": key, "mods": mods}
        if combo in self.active_keys:
            raise KeyError(f"Keypress action with keypresses {combo} already exists")
        self.active_keys[combo] = (name, action)

    def deregister_key(self, key: int, mods: int, name: str):
        combo: dict[str, int] = {"key": key, "mods": mods}
        if combo not in self.active_keys:
            raise KeyError(f"Keypress action with keypresses {combo} does not exist, therefore cannot be deregistered.")
        if self.active_keys[combo][0] != name:
            raise KeyError(f"Keypress listener with name {name} not found. Have you registered it yet?")
        del self.active_keys[combo]

    def register_click_listener(self, target: pygame.Surface, name: str, action: Callable[[], None]) -> None:
        if target in self.clickables:
            raise KeyError(f"Could not add click listener {name}, because the attached Surface already has a listener.")
        self.clickables[target] = (name, action)

    def deregister_click_listener(self, target: pygame.Surface, name: str) -> None:
        if target not in self.clickables:
            raise KeyError(f"Click listener for a Surface, with {name} name, has not been registered. Please register it first.")
        if self.clickables[target][0] != name:
            raise KeyError(f"Click listener has already been registered, albeit with a separate name. Please use {self.clickables[target][0]} as the name to deregister it.")
        del self.clickables[target]
