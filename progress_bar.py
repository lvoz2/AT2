from typing import Any, Optional

import pygame

import element
import sprite


class ProgressBar(element.Element):
    def __init__(
        self,
        max_value: float,
        rect: pygame.Rect,
        rect_options: dict[str, Any],
        visible: bool = True,
        value: Optional[float] = None,
    ) -> None:
        self.max_width = rect.width
        self.max_value = max_value
        design = sprite.Sprite(rect=rect, rect_options=rect_options)
        super().__init__(
            design,
            mask=pygame.Rect(
                0,
                0,
                (
                    rect.width
                    if value is None
                    else self.max_width * (value / self.max_value)
                ),
                rect.height,
            ),
            visible=visible,
        )

    def update(self, new_value: int) -> None:
        if self.mask is not None:
            self.mask.width = int(self.max_width * (new_value / self.max_value))
