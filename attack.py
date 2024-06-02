from typing import Optional
from effect import Effect
from entity import Entity


class Attack:
	def __init__(self, dmg: int, cost: int, effects: Optional[dict[str, Effect]] = None) -> None:
		self.dmg = dmg
		self.cost = cost
		self.effects = effects
		self.duration = 0
		if self.effects is not None and len(self.effects) != 0:
			for value in self.effects.values():
				if value.duration > self.duration:
					self.duration = value.duration

	def has_effects(self) -> bool:
		return self.effects is not None and len(self.effects) != 0

	def damage(self, target: Entity):
		target.damage(self.dmg)

	def apply_effects(self, target: Entity, delta: int) -> None:
		if self.effects is not None:
			self.duration -= delta
			self.duration = max(self.duration, 0)
			for key, value in self.effects.items():
				if value.is_finished():
					del self.effects[key]
				else:
					value.damage(target, delta)
					if value.is_finished():
						del self.effects[key]
