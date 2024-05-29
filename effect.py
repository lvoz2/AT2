from entity import Entity

class Effect:
    def __init__(self, name: str, duration: int, dps: int) -> None:
        self.name = name
        self.duration = duration
        self.dps = dps
    
    def is_finished(self) -> bool:
        return duration <= 0
    
    def damage(self, target: Entity, delta: int) -> None:
        seconds: float = 0
        if delta < self.duration:
            self.duration -= delta
            seconds = delta / 100
        else:
            seconds = self.duration / 1000
        target.damage(self.dps * seconds)