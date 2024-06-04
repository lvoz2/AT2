import enemy
import assets


class Zombie(enemy.Enemy):
    def __init__(self, x: int, y: int, name: str, scale: int = 1):
	    super().__init__(assets.GAME_ASSETS["skeleton"], x, y, name, 0.1, scale)