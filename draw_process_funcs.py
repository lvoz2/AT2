import pathlib
from typing import Any, Literal, Optional, Sequence

import pygame


def init(dim: Sequence[int]) -> None:
    pygame.init()
    global window  # pylint: disable=global-variable-undefined
    window = pygame.display.set_mode(dim)  # type: ignore[name-defined]
    pygame.key.set_repeat(25)


def construct_and_blit(
    surf_as_bytes: tuple[
        bytes,
        Sequence[int] | tuple[int, int],
        Literal["P", "RGB", "BGR", "BGRA", "RGBX", "RGBA", "ARGB"],
    ],
    rect: pygame.Rect,
    mask: Optional[pygame.Rect] = None,
) -> pygame.Rect:
    global window  # pylint: disable=global-variable-not-assigned
    surf: pygame.Surface = pygame.image.frombuffer(
        surf_as_bytes[0],
        surf_as_bytes[1],
        surf_as_bytes[2],
    )
    return window.blit(surf, rect, mask)  # type: ignore[name-defined]


def fill_screen(colour: Sequence[int] | tuple[int, int, int]) -> pygame.Rect:
    global window  # pylint: disable=global-variable-not-assigned
    return window.fill(color=colour)  # type: ignore[name-defined]


def load_image(
    path: pathlib.Path | str,
) -> tuple[
    bytes,
    Sequence[int] | tuple[int, int],
    Literal["P", "RGB", "BGR", "BGRA", "RGBX", "RGBA", "ARGB"],
]:
    surf: pygame.Surface = pygame.image.load(path)
    surf = surf.convert_alpha()
    return (
        pygame.image.tobytes(surf, "RGBA"),
        [surf.get_width(), surf.get_height()],
        "RGBA",
    )


def convert(
    surf_as_bytes: tuple[
        bytes,
        Sequence[int] | tuple[int, int],
        Literal["P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA"],
    ]
) -> tuple[
    bytes,
    Sequence[int] | tuple[int, int],
    Literal["P", "RGB", "RGBX", "RGBA", "ARGB", "BGRA"],
]:
    surf: pygame.Surface = pygame.image.frombuffer(
        surf_as_bytes[0],
        surf_as_bytes[1],
        surf_as_bytes[2],
    )
    surf = surf.convert_alpha()
    return (
        pygame.image.tobytes(surf, surf_as_bytes[2]),
        [surf.get_width(), surf.get_height()],
        surf_as_bytes[2],
    )


def get_events() -> list[tuple[int, dict[str, Any]]]:
    events: list[pygame.event.Event] = pygame.event.get()
    return [(evt.type, evt.dict) for evt in events]
