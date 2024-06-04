from player import Player
from assets import GAME_ASSETS


class Rogue(Player):
    def __init__(self, x: int, y: int, name: str, scale: int = 1):
        super().__init__(GAME_ASSETS["rogue"], x, y, name, "rogue", scale, defense=15)
        # Additional attributes and methods specific to the Rogue class
