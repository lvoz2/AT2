import player
import assets


class Mage(player.Player):
    def __init__(self, x: int, y: int, name: str, scale: float = 1) -> None:
        super().__init__(assets.get_asset("mage"), x, y, name, "mage", scale, mana=15)
