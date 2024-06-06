from typing import Optional, Sequence
import pygame
import surf_rect


class UI_Element:
    def __init__(self, design: surf_rect.Surf_Rect | str, x: Optional[int] = None, y: Optional[int] = None, font: Optional[pygame.font.Font] = None, anti_alias: Optional[bool] = None, fcolour: Optional[Sequence[int]] = None, bcolour: Optional[Sequence[int]] = None, center: bool = False, rect: Optional[pygame.Rect] = None, scale: int = 1) -> None:
        if isinstance(design, str):
            if font is not None and anti_alias is not None and fcolour is not None:
                surf = font.render(design, anti_alias, fcolour, bcolour)
                self.design: surf_rect.Surf_Rect = surf_rect.Surf_Rect(surf, surf.get_rect())
        else:
            self.design: surf_rect.Surf_Rect = design  # type: ignore  # This line may or may not actually get called, because it is wrapped in an if-else. Otherwise, mypy thinks I'm trying to redefine something that hasn't been defined yet
        print(self.design.surf.get_height())
        print(self.design.surf.get_width())
        self.design.surf = pygame.transform.scale(self.design.surf, (int(self.design.surf.get_width() * scale), int(self.design.surf.get_height() * scale)))
        self.x = x if x is not None else self.design.rect.x
        self.y = y if y is not None else self.design.rect.y
        self.center = center
        self.rect = rect

    def draw(self, window: pygame.Surface) -> None:
        if self.center:
            self.design.rect.center = (self.x, self.y)
            self.design.rect = window.blit(self.design.surf, self.design.rect(center=[self.x, self.y]), self.rect)
        else:
            self.design.rect = window.blit(self.design.surf, [self.x, self.y], self.rect)
