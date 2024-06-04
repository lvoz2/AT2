import player
import assets


class Mage(player.Player):
    def __init__(self, x: int, y: int, name: str, scale: int = 1) -> None:
        super().__init__(assets.GAME_ASSETS["mage"], x, y, name, "mage", scale, mana=15)
