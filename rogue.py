import player
import assets


class Rogue(player.Player):
    def __init__(self, x: int, y: int, name: str, scale: float = 1):
        super().__init__(
            assets.get_asset("rogue"), x, y, name, "rogue", scale, defense=15
        )
        # Additional attributes and methods specific to the Rogue class
