import copy
from typing import Any, Optional

import pygame


class Sprite:
    def __init__(
        self,
        surf: Optional[pygame.Surface],
        rect: pygame.Rect,
        scale: float = 1.0,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
    ) -> None:
        self.__surf = surf
        self.rect = rect
        self.change_design(surf, rect, scale, rect_options, font_options)

    @property
    def surf(self) -> pygame.Surface:
        if self.__surf is not None:
            return self.__surf
        raise ValueError("This sprite's surface is invalid")

    @surf.setter
    def surf(self, new_surf: pygame.Surface) -> None:
        self.__surf = new_surf

    def clone(self) -> "Sprite":
        cloned: "Sprite" = copy.deepcopy(self)
        if self.surf is not None:
            cloned.surf = self.surf.copy()
        cloned.rect = self.rect.copy()
        return cloned

    def __get_val_from_dict(
        self, dictionary: Optional[dict[Any, Any]], key: Any, default: Any = None
    ) -> Any:
        if dictionary is None:
            return default
        if key in dictionary:
            return dictionary[key]
        return default

    def change_design(
        self,
        surf: Optional[pygame.Surface],
        rect: pygame.Rect,
        scale: float,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
    ) -> None:
        self.rect = rect
        self.is_rect: bool = surf is None
        self.has_text: bool = font_options is not None
        if self.is_rect:
            self.colour = self.__get_val_from_dict(rect_options, "colour")
            self.colour = (
                self.colour
                if self.colour is not None
                else self.__get_val_from_dict(rect_options, "color")
            )
            self.color = self.colour
            self.surf = pygame.Surface((self.rect.width, self.rect.height))
            self.surf.fill(self.colour)
        elif self.has_text:
            self.font = self.__get_val_from_dict(font_options, "font")
            self.text = self.__get_val_from_dict(font_options, "text")
            self.anti_alias = self.__get_val_from_dict(font_options, "anti_alias", True)
            self.colour = self.__get_val_from_dict(font_options, "colour")
            self.colour = (
                self.colour
                if self.colour is not None
                else self.__get_val_from_dict(font_options, "color")
            )
            self.color = self.colour
            self.background = self.__get_val_from_dict(font_options, "background")
            self.surf = self.font.render(
                self.text, self.anti_alias, self.colour, self.background
            )
        elif surf is not None:
            self.surf = surf
        else:
            raise TypeError("Argument 1 is not a Surface, Rect, or string")
        if self.surf is not None:
            self.surf = pygame.transform.scale(
                self.surf.convert_alpha(),
                (
                    int(self.rect.width * scale),
                    int(self.rect.height * scale),
                ),
            )
