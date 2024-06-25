import copy
from typing import Any, Optional
import pathlib

import pygame


class Sprite:
    def __init__(
        self,
        surf: Optional[pygame.Surface] = None,
        rect: Optional[pygame.Rect] = None,
        scale: float = 1.0,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        path: Optional[pathlib.Path] = None
    ) -> None:
        self.__surf = surf
        self.__rect = rect
        self.rect_options = rect_options
        self.path = path
        self.change_design(surf, rect, scale, rect_options, font_options)

    @property
    def surf(self) -> pygame.Surface:
        if self.__surf is not None:
            return self.__surf
        raise ValueError("This sprite's surface is invalid")

    @surf.setter
    def surf(self, new_surf: pygame.Surface) -> None:
        self.__surf = new_surf.convert_alpha()

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is not None:
            return self.__rect
        raise ValueError("No rect has been associated with this sprite")

    @rect.setter
    def rect(self, new_rect: pygame.Rect) -> None:
        self.__rect = new_rect

    def clone(self) -> pygame.Surface:
        if self.surf is not None:
            return self.surf.copy()
        raise ValueError("No Surface associated with this sprite")

    def __get_val_from_dict(
        self,
        dictionary: Optional[dict[Any, Any]],
        key: Any,
        default: Any = None,
        error: bool = False,
    ) -> Any:
        if dictionary is None:
            return default
        if key in dictionary:
            return dictionary[key]
        if error:
            raise KeyError(f"Key {key} not in dict {dictionary}")
        return default

    def change_design(
        self,
        surf: Optional[pygame.Surface],
        rect: Optional[pygame.Rect],
        scale: float,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
    ) -> None:
        if rect is not None:
            self.rect = rect
        self.is_rect: bool = surf is None
        self.has_text: bool = font_options is not None
        if self.has_text:
            self.font = self.__get_val_from_dict(font_options, "font")
            self.text = self.__get_val_from_dict(font_options, "text")
            self.anti_alias = self.__get_val_from_dict(font_options, "anti_alias", True)
            self.colour = self.__get_val_from_dict(font_options, "colour")
            self.colour = (
                self.colour
                if self.colour is not None
                else self.__get_val_from_dict(font_options, "color", default=(0, 0, 0))
            )
            self.color = self.colour
            self.background = self.__get_val_from_dict(font_options, "background")
            self.surf = self.font.render(
                self.text, self.anti_alias, self.colour, self.background
            )
            self.rect = rect if rect is not None else self.surf.get_rect()
        elif self.is_rect:
            if rect is None:
                raise ValueError("A Rect must be provided if no Surface is provided")
            self.colour = self.__get_val_from_dict(rect_options, "colour")
            self.colour = (
                self.colour
                if self.colour is not None
                else self.__get_val_from_dict(rect_options, "color")
            )
            self.color = self.colour
            self.surf = pygame.Surface((self.rect.width, self.rect.height))
            self.surf.fill(self.colour)
        elif surf is not None:
            self.surf = surf
            if rect is None:
                self.rect = self.surf.get_rect()
                self.surf = self.scale(scale)
            else:
                self.surf, self.rect = self.scale(scale), rect
        else:
            raise TypeError("No argument given to create a Surface")
        self.center = self.__get_val_from_dict(rect_options, "center", False)
        x: int = self.__get_val_from_dict(rect_options, "x", default=0, error=True)
        y: int = self.__get_val_from_dict(rect_options, "y", default=0, error=True)
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.left = x
            self.rect.top = y

    def scale(self, scale: float) -> pygame.Surface:
        new_dimensions: tuple[int, int] = (
            int(self.rect.width * scale),
            int(self.rect.height * scale),
        )
        self.rect.update(self.rect.x, self.rect.y, new_dimensions[0], new_dimensions[1])
        return pygame.transform.scale(
                self.surf,
                (
                    new_dimensions[0],
                    new_dimensions[1],
                ),
            )
