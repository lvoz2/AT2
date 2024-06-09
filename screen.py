from typing import Any, Callable, Optional
import pygame
import entity
import surf_rect
import ui_element


class Screen:
    def __init__(self, bground: pygame.Surface) -> None:
        self.bground = bground
        self.renderables = None
        self.listeners: dict[int, dict[Callable[..., None], Optional[dict[str, Any]]]]
        self.__active_keys: dict[
            tuple[int, int], tuple[str, Callable[..., None], dict[str, Any]]
        ] = {}
        self.__clickables: dict[
            surf_rect.Surf_Rect,
            tuple[str, Callable[..., None], dict[str, Any]],
        ] = {}
        self.entities: list[list[entity.Entity]] = [[]]
        self.ui: list[list[ui_element.UI_Element]] = [[]]

    @property
    def clickables(
        self,
    ) -> dict[surf_rect.Surf_Rect, tuple[str, Callable[..., None], dict[str, Any]]]:
        """Returns the targets that are listening for clicks"""
        return self.__clickables

    def register_key(
        self,
        name: str,
        key: int,
        mods: int,
        action: Callable[..., None],
        *args,
        **kwargs,
    ) -> None:
        combo: tuple[int, int] = (key, mods)
        if combo in self.__active_keys:
            raise KeyError(f"Keypress action with keypresses {combo} already exists")
        extras: dict[str, Any] = {"args": args, "kwargs": kwargs}
        self.__active_keys[combo] = (name, action, extras)

    def deregister_key(self, key: int, mods: int, name: str):
        combo: tuple[int, int] = (key, mods)
        if combo not in self.__active_keys:
            raise KeyError(
                f"Keypress action with keypresses {combo} does not exist, "
                "therefore cannot be deregistered."
            )
        if self.__active_keys[combo][0] != name:
            raise KeyError(
                f"Keypress listener with name {name} not found. Have you "
                "registered it yet?"
            )
        del self.__active_keys[combo]

    @property
    def active_keys(
        self,
    ) -> dict[tuple[int, int], tuple[str, Callable[..., None], dict[str, Any]]]:
        """Returns the current actively listened to keys"""
        return self.__active_keys

    def register_click_listener(
        self,
        target: surf_rect.Surf_Rect,
        name: str,
        action: Callable[..., None],
        *args,
        **kwargs,
    ) -> None:
        if target in self.__clickables:
            raise KeyError(
                f"Could not add click listener {name}, because the attached "
                "Surface already has a listener."
            )
        self.__clickables[target] = (
            name,
            action,
            {"args": args, "kwargs": kwargs},
        )

    def deregister_click_listener(self, target: surf_rect.Surf_Rect, name: str) -> None:
        if target not in self.__clickables:
            raise KeyError(
                f"Click listener for a Surface, with {name} name, has not been"
                " registered. Please register it first."
            )
        if self.__clickables[target][0] != name:
            raise KeyError(
                "Click listener has already been registered, albeit with a"
                f" separate name. Please use {self.__clickables[target][0]} as"
                " the name to deregister it."
            )
        del self.__clickables[target]
