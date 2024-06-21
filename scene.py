import element
import sprite


class Scene(element.Element):
    def __init__(self, bground: sprite.Sprite) -> None:
        super().__init__(bground)
        self.renderables = None
        self.elements: list[list[element.Element]] = [[]]
