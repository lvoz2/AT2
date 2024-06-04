from player import Player
from assets import GAME_ASSETS


class Mage(Player):
    def __init__(self, x: int, y: int, name: str, scale: int = 1) -> None:
        super().__init__(GAME_ASSETS["mage"], x, y, name, "mage", scale, mana=15)
