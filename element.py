from typing import Any, Callable, Optional, Sequence

import pygame

import sprite


class Element:
    def __init__(
        self,
        design: sprite.Sprite | str,
        mask: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        scale: float = 1.0,
        visible: bool = False,
    ) -> None:
        if isinstance(design, str):
            if font_options is not None:
                font: pygame.font.Font = self.__get_val_from_dict(
                    font_options, "font", None
                )
                anti_alias: bool = self.__get_val_from_dict(
                    font_options, "anti_alias", True
                )
                fcolour: str | Sequence[int] = self.__get_val_from_dict(
                    font_options, "fcolour", [0, 0, 0]
                )
                bcolour: str | Sequence[int] = self.__get_val_from_dict(
                    font_options, "bcolour", [255, 255, 255]
                )
                surf: pygame.Surface = font.render(design, anti_alias, fcolour, bcolour)
                self.design: sprite.Sprite = sprite.Sprite(
                    surf, surf.get_rect()
                )
        elif isinstance(design, sprite.Sprite):
            self.design = design
        self.mask = mask
        self.design.surf = pygame.transform.scale(
            self.design.surf.convert_alpha(),
            (
                int(self.design.rect.width * scale),
                int(self.design.rect.height * scale),
            ),
        )
        self.listeners: dict[
            int, dict[Callable[..., None], Optional[dict[str, Any]]]
        ] = {}
        self.x = self.__get_val_from_dict(rect_options, "x", self.design.rect.x)
        self.y = self.__get_val_from_dict(rect_options, "y", self.design.rect.y)
        self.visible = visible
        self.rect_options = rect_options

    # def update_design(new_design)

    def __get_val_from_dict(
        self, dictionary: Optional[dict[Any, Any]], key: Any, default: Any = None
    ) -> Any:
        if dictionary is None:
            return default
        if key in dictionary:
            return dictionary[key]
        return default

    def register_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type not in self.listeners:
            self.listeners[event_type] = {}
        if options is None:
            options = {}
        options["target"] = self
        self.listeners[event_type][func] = options

    def deregister_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
        if event_type not in self.listeners:
            raise KeyError(
                "No event listeners created yet for event type "
                f"{event_type}. Function: {func}"
            )
        if func not in self.listeners[event_type]:
            raise KeyError(
                "Event listener does not exist. Event Type: "
                f"{event_type}, Function: {func}"
            )
        if self.listeners[event_type][func] != options:
            raise ValueError(
                "The options argument provided did not match what was expected. "
                f"Expected {self.listeners[event_type][func]}, "
                f"received {options}"
            )
        del self.listeners[event_type][func]

    def draw(self, window: pygame.Surface) -> None:
        if self.__get_val_from_dict(self.rect_options, "center", False):
            self.design.rect.center = (self.x, self.y)
            self.design.rect = window.blit(
                self.design.surf, self.design.rect, self.mask
            )
        else:
            self.design.rect = window.blit(
                self.design.surf, [self.x, self.y], self.mask
            )
