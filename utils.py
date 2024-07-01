import concurrent.futures as cf
import concurrent.futures._base as cf_b
import concurrent.futures.process as cf_p
import multiprocessing as mp
import multiprocessing.context as mp_c
import pathlib
from typing import Any, Callable, Literal, Optional, Sequence

import pygame

import draw_process_funcs as dpf
import sprite

__assets: dict[str, sprite.Sprite] = {}


class AsyncRunner:
    def __init__(
        self,
        name: str,
        start_method: str = "fork",
        initfunc: Optional[Callable[..., None]] = None,
        initargs: tuple[Any, ...] = (),
    ) -> None:
        self.start_method = start_method
        self.__ctx: mp_c.BaseContext = mp.get_context(self.start_method)
        self.executor: cf_p.ProcessPoolExecutor = cf.ProcessPoolExecutor(
            max_workers=1,
            mp_context=self.__ctx,
            initializer=initfunc,
            initargs=initargs,
        )
        runners[name] = self


runners: dict[str, AsyncRunner] = {}


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
            is_async=__assets[posix_path].is_async,
            executor=__assets[posix_path].executor,
        )
    if "display" not in runners:
        surf: pygame.Surface = pygame.image.load(absolute_path).convert_alpha()
        design: sprite.Sprite = sprite.Sprite(
            surf, rect, rect_options=rect_options, scale=scale, path=absolute_path
        )
    else:
        load_fut: cf_b.Future = runners["display"].executor.submit(
            dpf.load_image, absolute_path
        )
        cf.wait([load_fut])
        res: tuple[
            bytes,
            Sequence[int] | tuple[int, int],
            Literal["P", "RGB", "BGR", "BGRA", "RGBX", "RGBA", "ARGB"],
        ] = load_fut.result()
        surf = pygame.image.frombuffer(res[0], res[1], res[2])
        design = sprite.Sprite(
            surf,
            rect,
            rect_options=rect_options,
            scale=scale,
            path=absolute_path,
            is_async=True,
            executor=runners["display"].executor,
        )
    __assets[posix_path] = design
    return design


class Singleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]
