import pathlib
from typing import Any, Optional

import pygame

import sprite

__assets: dict[str, sprite.Sprite] = {}


def get_asset(
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
    if posix_path in __assets:
        return sprite.Sprite(
            __assets[posix_path].clone(),
            rect,
            rect_options=rect_options,
            scale=scale,
        )
    surf: pygame.Surface = pygame.image.load(absolute_path).convert_alpha()
    design: sprite.Sprite = sprite.Sprite(
        surf, rect, rect_options=rect_options, scale=scale, path=absolute_path
    )
    __assets[posix_path] = design
    return design
