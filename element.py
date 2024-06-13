from typing import Any, Optional, Sequence
import pygame
import surf_rect


class Element(object):
    def __init__(self, design: surf_rect.Surf_Rect | str, mask: Optional[pygame.Rect] = None, rect_options: Optional[dict[str, Any]] = None, font_options: Optional[dict[str, Any]] = None, scale: float = 1.0) -> None:
        if isinstance(design, str):
            if font_options is not None:
                font: pygame.font.Font = self.__get_val_from_dict(font_options, "font", None)
                anti_alias: bool = self.__get_val_from_dict(font_options, "anti_alias", True)
                fcolour: str | Sequence[int] = self.__get_val_from_dict(font_options, "fcolour", [0, 0, 0])
                bcolour: str | Sequence[int] = self.__get_val_from_dict(font_options, "bcolour", [255, 255, 255])
                surf: pygame.Surface = font.render(design, anti_alias, fcolour, bcolour)
                self.design: surf_rect.Surf_Rect = surf_rect.surf_rect(surf, surf.get_rect())
        elif isinstance(design, surf_rect.Surf_Rect):
            self.design = design
        self.mask = mask

    # def update_design(new_design)

    def __get_val_from_dict(self, dict, key, default = None) -> Any:
        if key in dict:
            return dict[key]
        return default

    def register_listener(
        self,
        event_type: int,
        func: Callable[..., None],
        options: Optional[dict[str, Any]] = None,
    ) -> None:
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
                f"Expected {self.__cur_screen.listeners[event_type][func]}, "
                f"received {options}"
            )
        del self.listeners[event_type][func]