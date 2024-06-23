from typing import Optional

import effect
import entity


class Attack:
    def __init__(
        self,
        dmg: int,
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

    def damage(self, target: entity.Entity, event_id: int) -> None:
        target.damage(self.dmg, event_id)

    def apply_effects(self, target: entity.Entity, delta: int, event_id: int) -> None:
        if self.effects is not None:
            self.duration -= delta
            self.duration = max(self.duration, 0)
            for key, value in self.effects.items():
                if value.is_finished():
                    del self.effects[key]
                else:
                    value.damage(target, delta, event_id)
                    if value.is_finished():
                        del self.effects[key]
