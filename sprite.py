import concurrent.futures as cf
import concurrent.futures._base as cf_b
import concurrent.futures.process as cf_p
import pathlib
from typing import Any, Optional

import pygame

import draw_process_funcs as dpf


class Sprite:
    def __init__(
        self,
        surf: Optional[pygame.Surface] = None,
        rect: Optional[pygame.Rect] = None,
        scale: float = 1.0,
        rect_options: Optional[dict[str, Any]] = None,
        font_options: Optional[dict[str, Any]] = None,
        path: Optional[pathlib.Path] = None,
        is_async: bool = False,
        executor: Optional[cf_p.ProcessPoolExecutor] = None,
    ) -> None:
        self.is_async = is_async
        if self.is_async and executor is None:
            raise TypeError("An executor must be provided to do asynchronous execution")
        self.executor = executor
        self.__surf = surf
        self.__rect = rect
        self.rect_options = rect_options
        self.path = path
        if self.__rect is None:
            self.__x: int = 0
            self.__y: int = 0
            self.__width: int = 0
            self.__height: int = 0
        else:
            self.__x = self.__rect.x
            self.__y = self.__rect.y
            self.__width = self.__rect.width
            self.__height = self.__rect.height
        self.change_design(surf, rect, scale, rect_options, font_options)

    @property
    def surf(self) -> pygame.Surface:
        if self.__surf is not None:
            return self.__surf
        raise ValueError("This sprite's surface is invalid")

    @surf.setter
    def surf(self, new_surf: pygame.Surface) -> None:
        if self.is_async:
            if self.executor is None:
                raise TypeError(
                    "An executor must be provided to do asynchronous execution"
                )
            fut: cf_b.Future = self.executor.submit(
                dpf.convert,
                (
                    pygame.image.tobytes(new_surf, "RGBA"),
                    [new_surf.get_width(), new_surf.get_height()],
                    "RGBA",
                ),
            )
            cf.wait([fut])
            res = fut.result()
            self.__surf = pygame.image.frombuffer(res[0], res[1], res[2])
        else:
            self.__surf = new_surf.convert_alpha()

    @property
    def rect(self) -> pygame.Rect:
        if self.__rect is not None:
            return self.__rect
        raise ValueError("No rect has been associated with this sprite")

    @rect.setter
    def rect(self, new_rect: pygame.Rect) -> None:
        self.__rect = new_rect
        self.x = new_rect.x
        self.y = new_rect.y
        self.width = new_rect.width
        self.height = new_rect.height

    @property
    def x(self) -> int:
        return self.__x

    @x.setter
    def x(self, new_x: int) -> None:
        self.__x = new_x
        self.rect.x = new_x

    @property
    def y(self) -> int:
        return self.__y

    @y.setter
    def y(self, new_y: int) -> None:
        self.__y = new_y
        self.rect.y = new_y

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, new_width: int) -> None:
        self.__width = new_width
        self.rect.width = new_width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, new_height: int) -> None:
        self.__height = new_height
        self.rect.height = new_height

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
                else self.__get_val_from_dict(rect_options, "color", error=True)
            )
            self.color = self.colour
            self.surf = pygame.Surface((self.width, self.height))
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
        x: int = self.__get_val_from_dict(rect_options, "x", default=self.rect.x)
        y: int = self.__get_val_from_dict(rect_options, "y", default=self.rect.y)
        if self.center:
            self.rect.center = (x, y)
        else:
            self.rect.x = x
            self.rect.y = y

    def scale(self, scale: float) -> pygame.Surface:
        new_dimensions: tuple[int, int] = (
            int(self.width * scale),
            int(self.height * scale),
        )
        self.rect.update(self.x, self.y, new_dimensions[0], new_dimensions[1])
        self.rect = self.rect
        scaled: pygame.Surface = pygame.transform.scale(
            self.surf,
            (
                new_dimensions[0],
                new_dimensions[1],
            ),
        )
        return scaled
