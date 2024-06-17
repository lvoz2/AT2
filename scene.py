import element
import surf_rect


class Scene(element.Element):
    def __init__(self, bground: surf_rect.Surf_Rect) -> None:
        super().__init__(bground)
        self.renderables = None
        self.elements: list[list[element.Element]] = [[]]
