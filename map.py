import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy


class Map:
    def __init__(self, window) -> None:
        """
        Initialize the Map class.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.window = window
        self.map_image: pygame.Surface = GAME_ASSETS["dungeon_map"].convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images: dict[str, pygame.Surface] = {
            "Warrior": GAME_ASSETS["warrior"].convert_alpha(),
            "Mage": GAME_ASSETS["mage"].convert_alpha(),
            "Rogue": GAME_ASSETS["rogue"].convert_alpha()
        }
        self.player_type = None
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Enemy(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
        ]
        self.in_combat = False  # Ensure this attribute is defined in the constructor
        self.current_enemy = None
        self.blue_orb = None
        self.game_over = False
        self.delta: list[int] = []
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def load_player(self, character_type):
        """
        Load the player character.

        Args:
            character_type (str): The type of character to load.
        """
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))

    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.

        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.enemies:
            if self.calculate_distance([enemy.position[0], enemy.position[1], enemy.image], [self.player_position[0], self.player_position[1], self.player_image])[0] < 1:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def handle_combat(self):
        """
        Handle combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(5, 10)
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                # Assume player has a method to take damage
                # self.player.take_damage(enemy_damage)

    def spawn_blue_orb(self):
        """
        Spawn the blue orb in the center of the map.
        """
        self.blue_orb = GAME_ASSETS["blue_orb"].convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.

        Returns:
            bool: True if the player has collided with the blue orb, False otherwise.
        """
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            self.game_over = True
            print("YOU WIN")  # This can be modified to a more visual display if needed.
            return True
        return False

    def handle_events(self):
        """
        Handle user input events.

        Returns:
            str: "quit" if the game is over and should be exited, None otherwise.
        """
        if self.game_over:
            return "quit"  # Stop processing events if game is over

        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT]:
            self.player_position[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            self.player_position[0] += move_speed
        if keys[pygame.K_UP]:
            self.player_position[1] -= move_speed
        if keys[pygame.K_DOWN]:
            self.player_position[1] += move_speed

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()

        if self.blue_orb and self.check_orb_collision():
            return "quit"

    def draw(self):
        """
        Draw the game objects on the window.
        """
        self.delta = self.clock.tick()
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
        for enemy in self.enemies:
            enemy.draw()
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        pygame.display.flip()
