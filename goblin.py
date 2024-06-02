import pygame
import helpers


class Goblin:
    def __init__(self, position, window):
        # Load the goblin image from the specified path
        self.image = pygame.image.load("AT2/assets/goblin.png").convert_alpha()  # Ensure the image path is correct
        self.position = position  # Store the initial position of the goblin
        self.window = window  # Store the game window object

    def move(self):
        # Move the goblin randomly within a specified range
        self.position[0] += helpers.randint(-10, 10)  # Randomly change the x-coordinate
        self.position[1] += helpers.randint(-10, 10)  # Randomly change the y-coordinate

        # Ensure the goblin stays within the bounds of the window
        self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))  # Clamp the x-coordinate
        self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))  # Clamp the y-coordinate

    def draw(self):
        # Draw the goblin on the game window
        self.window.blit(self.image, self.position)
