import pathlib
import copy
from typing import Any, Optional

import pygame

import surf_rect


def __iterate_files(directory: pathlib.Path, image_types: list[str]) -> Any:
    """
        Iterates over files in a directory adding them
        to the game assets. Recursively calls itself when
        a sub-directory is found
    Args:
        directory (Path): Path to sub-directory
        image_types (list of strings): tuple of valid image file types
    """
    # I'm not giving this an explicit type hint because it will end up being an
    # n-dimensional dict, where n could be any number
    assets: Any = {}
    for item in pathlib.Path.iterdir(directory):
        if item.is_file() and item.suffix in image_types:
            surf: pygame.Surface = pygame.image.load(item).convert_alpha()
            rect: pygame.Rect = surf.get_rect()
            assets[item.stem] = surf_rect.Surf_Rect(surf, rect)

        # if a sub-folder is found
        elif item.is_dir():
            assets[item.name] = __iterate_files(item, image_types)
    return assets


def load_assets(assetdir: str) -> Any:
    """
    Searches the local directory for assets
    using current working directory.
    """
    pygame.display.init()
    pygame.display.set_mode([1920, 1080])
    # Constants
    cwd: pathlib.Path = pathlib.Path.cwd()
    assets_folder: pathlib.Path = pathlib.Path.joinpath(cwd, assetdir)
    image_types: list[str] = [".jpg", ".png"]
    # Verify assets folder exists
    if not assets_folder.exists():
        raise FileNotFoundError(f"Assets directory not found: {assets_folder}")
    # Iterate over files in the directory adding    \
    #   each image to the dictionary. Images will  \
    #   be added by the file name, sans the suffix
    res: Any = __iterate_files(assets_folder, image_types)
    pygame.display.quit()
    return res


__GAME_ASSETS = load_assets("assets")


def get_asset(*args) -> Any:
    asset: Optional[Any] = None
    for key in args:
        asset = __GAME_ASSETS[key]
    if isinstance(asset, surf_rect.Surf_Rect):
        return surf_rect.Surf_Rect(asset.surf.copy(), asset.rect.copy())
    return asset
