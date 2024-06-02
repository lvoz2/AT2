import pygame
import helpers


class Orc:
    def __init__(self, position, window):
        # Load the orc image from the specified path
        self.image = pygame.image.load("AT2/assets/orc.png").convert_alpha()  # Ensure the image path is correct
        self.position = position  # Store the initial position of the orc
        self.window = window  # Store the window object to draw the orc on

    def move(self):
        # Move the orc randomly within a specified range
        self.position[0] += helpers.randint(-20, 20)  # Randomly change the x-coordinate
        self.position[1] += helpers.randint(-20, 20)  # Randomly change the y-coordinate

        # Ensure the orc stays within the bounds of the window
        self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))  # Clamp the x-coordinate
        self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))  # Clamp the y-coordinate

    def draw(self):
        # Draw the orc on the window at its current position
        self.window.blit(self.image, self.position)
