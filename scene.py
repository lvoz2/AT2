from typing import Iterator

import element
import sprite


class Scene(element.Element):
    def __init__(self, bground: sprite.Sprite) -> None:
        super().__init__(bground)
        self.renderables = None
        self.elements: list[list[element.Element]] = [[]]

    @property
    def visible_elements(self) -> Iterator[element.Element]:
        for element_layer in self.elements:
            for e in element_layer:
                if e.visible:
                    yield e
