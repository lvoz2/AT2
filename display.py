import pathlib
import sys
from typing import Any, Optional, Sequence

import pygame

import event_processors
import events
import scene
import singleton
import sprite


class Display(metaclass=singleton.Singleton):
    def __init__(self, title: str = "", dim: Sequence[int] = (0, 0)) -> None:
        if not hasattr(self, "created"):
            self.screens: dict[str, scene.Scene] = {}
            self.cur_screen: Optional[scene.Scene] = None
            pygame.init()
            self.window = pygame.display.set_mode(dim)
            pygame.display.set_caption(title)
            pygame.key.set_repeat(25)
            self.clock: pygame.time.Clock = pygame.time.Clock()
            self.delta: list[int] = [0]
            self.game_over: bool = False
            self.events = events.Events()
            event_processors.load()
            self.created: bool = True
            self.__assets: dict[str, sprite.Sprite] = {}

    def get_asset(
        self,
        asset_location: str,
        rect: Optional[pygame.Rect] = None,
        rect_options: Optional[dict[str, Any]] = None,
        scale: float = 1.0,
    ) -> sprite.Sprite:
        absolute_path: pathlib.Path = pathlib.Path.joinpath(
            pathlib.Path.cwd(), asset_location
        )
        if not absolute_path.exists() or not absolute_path.is_file():
            raise FileNotFoundError(f"Image file not found: {absolute_path}")
        valid_types: list[str] = [
            ".bmp",
            ".gif",
            ".jpeg",
            ".jpg",
            ".lbm",
            ".pbm",
            ".pgm",
            ".ppm",
            ".pcx",
            ".png",
            ".pnm",
            ".svg",
            ".tga",
            ".tiff",
            ".tif",
            ".webp",
            ".xpm",
        ]
        if absolute_path.suffix not in valid_types:
            raise RuntimeError(
                f"The file {absolute_path} does not have an appropriate extension/type"
            )
        posix_path: str = absolute_path.as_posix()
        if posix_path in self.__assets:
            return sprite.Sprite(
                self.__assets[posix_path].clone(),
                rect,
                rect_options=rect_options,
                scale=scale,
            )
        surf: pygame.Surface = pygame.image.load(absolute_path).convert_alpha()
        design: sprite.Sprite = sprite.Sprite(
            surf, rect, rect_options=rect_options, scale=scale
        )
        self.__assets[posix_path] = design
        return design

    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens:
            event_processor: events.Events = events.Events()
            event_processor.cur_screen = self.screens[new_screen]
            self.cur_screen = self.screens[new_screen]
        else:
            raise KeyError(
                f'Screen with identifier "{new_screen}" not \
            found, either because it does not exist or has \
            not been loaded into the Display'
            )

    def add_screen(self, name: str, new_screen: scene.Scene) -> bool:
        if name not in self.screens:
            self.screens[name] = new_screen
        else:
            raise KeyError(
                "Screen couldn't be added, becuase another Screen with the "
                "same name already loaded. Find a different name and try again"
            )
        return name in self.screens

    def handle_events(self) -> None:
        if self.cur_screen is not None:
            self.draw()
            for e in pygame.event.get():
                self.events.notify(e)

    def update(self, delta: list[int]) -> None:
        pass

    def draw(self) -> None:
        if self.cur_screen is not None:
            self.delta.append(self.clock.tick_busy_loop(25))
            if len(self.delta) > 10:
                self.delta = self.delta[(len(self.delta) - 10) :]
            self.window.fill([0, 0, 0])
            self.cur_screen.design.rect = self.window.blit(
                self.cur_screen.design.surf, [0, 0]
            )
            if self.cur_screen.elements != [None]:
                for element_layer in self.cur_screen.elements:
                    for element in element_layer:
                        element.draw(self.window)
            self.update(self.delta)
            pygame.display.flip()
