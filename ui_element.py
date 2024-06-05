from typing import Optional
import pygame


class UI_Element:
    def __init__(self, design: pygame.Surface | str, x: int, y: int, font: Optional[pygame.font.Font] = None, anti_alias: Optional[bool] = None, fcolour: Optional[str] = None, bcolour: Optional[str] = None, center: bool = False) -> None:
        if isinstance(design, str):
            if font is not None and anti_alias is not None and fcolour is not None:
                self.design: pygame.Surface = font.render(design, anti_alias, fcolour, bcolour)
        else:
            self.design: pygame.Surface = design  # type: ignore  # This line may or may not actually get called, because it is wrapped in an if-else. Otherwise, mypy thinks I'm trying to redefine something that hasn't been defined yet
        self.x = x
        self.y = y
        self.center = center

    def draw(self, window: pygame.Surface) -> None:
        if self.center:
            window.blit(self.design, [self.x, self.y])
        else:
            window.blit(self.design, self.design.get_rect(center=[self.x, self.y]))
