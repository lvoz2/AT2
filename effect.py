from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import entity


class Effect:
    def __init__(self, name: str, duration: int, dps: int) -> None:
        self.name = name
        self.duration = duration
        self.dps = dps

    def is_finished(self) -> bool:
        return self.duration <= 0

    def damage(self, target: "entity.Entity", delta: int) -> None:
        seconds: float = 0
        if delta < self.duration:
            self.duration -= delta
            seconds = delta / 100
        else:
            seconds = self.duration / 1000
        target.damage(int(self.dps * seconds))
