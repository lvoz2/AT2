import player
import assets


class Rogue(player.Player):
    def __init__(self, x: int, y: int, name: str, scale: int = 1):
        super().__init__(
            assets.GAME_ASSETS["rogue"], x, y, name, "rogue", scale, defense=15
        )
        # Additional attributes and methods specific to the Rogue class
