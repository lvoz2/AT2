import copy
from typing import Any, Optional

import pygame


class Sprite:
    def __init__(
        self,
        surf: pygame.Surface,
        rect: pygame.Rect,
        rect_options: Optional[  # pylint: disable=unused-argument
            dict[str, Any]  # pylint: disable=unused-argument
        ] = None,  # pylint: disable=unused-argument
    ) -> None:
        self.surf = surf
        self.rect = rect

    def clone(self) -> "Sprite":
        cloned: "Sprite" = copy.deepcopy(self)
        cloned.surf = self.surf.copy()
        cloned.rect = self.rect.copy()
        return cloned
