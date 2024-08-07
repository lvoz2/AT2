from typing import Optional

import effect
import entity


class Attack:
    def __init__(
        self,
        dmg: float,
        cost: int,
        effects: Optional[dict[str, effect.Effect]] = None,
    ) -> None:
        self.dmg = dmg
        self.cost = cost
        self.effects = effects
        self.duration = 0
        if self.effects is not None and len(self.effects) != 0:
            for value in self.effects.values():
                self.duration = min(self.duration, value.duration)

    def has_effects(self) -> bool:
        return self.effects is not None and len(self.effects) != 0

    def damage(self, strength: int, target: entity.Entity) -> bool:
        return target.damage(round(self.dmg * strength))
        # del target

    def apply_effects(self, target: entity.Entity, delta: int) -> None:
        if self.effects is not None:
            self.duration -= delta
            self.duration = max(self.duration, 0)
            for key, value in self.effects.items():
                if value.is_finished():
                    del self.effects[key]
                else:
                    value.damage(
                        target,
                        delta,
                    )
                    if value.is_finished():
                        del self.effects[key]
