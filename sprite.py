import copy
from typing import Any, Optional

import pygame


class Sprite:
    def __init__(
        self,
        surf: Optional[pygame.Surface],
        rect: pygame.Rect,
        rect_options: Optional[
            dict[str, Any]
        ] = None,
        font_options: Optional[
            dict[str, Any]
        ] = None,
    ) -> None:
        self.change_design(surf, rect, rect_options, font_options)

    def clone(self) -> "Sprite":
        cloned: "Sprite" = copy.deepcopy(self)
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

    def change_design(self,
        surf: Optional[pygame.Surface],
        rect: pygame.Rect,
        rect_options: Optional[
            dict[str, Any]
        ] = None,
        font_options: Optional[
            dict[str, Any]
        ] = None
    ) -> None:
        self.surf = surf
        self.rect = rect
        self.is_rect: bool = surf is None
        if self.is_rect:
            self.colour = self.__get_val_from_dict(rect_options, "colour")
            self.colour = self.colour if self.colour is not None else self.__get_val_from_dict(rect_options, "color")
            self.color = self.colour
            self.surf = pygame.Surface((self.rect.width, self.rect.height))
            self.surf.fill(self.colour)
        self.has_text: bool = font_options is not None
        if self.has_text:
            self.font = self.__get_val_from_dict(font_options, "font")
            self.text = self.__get_val_from_dict(font_options, "text")
            self.anti_alias = self.__get_val_from_dict(font_options, "anti_alias", True)
            self.colour = self.__get_val_from_dict(font_options, "colour")
            self.colour = self.colour if self.colour is not None else self.__get_val_from_dict(font_options, "color")
            self.color = self.colour
            self.background = self.__get_val_from_dict(font_options, "background")