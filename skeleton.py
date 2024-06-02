import pygame
import helpers


class Skeleton:
	def __init__(self, position, window):
		# Load the skeleton image from the specified path
		self.image = pygame.image.load("AT2/assets/skeleton.png").convert_alpha()  # Ensure the image path is correct
		self.position = position  # Store the initial position of the skeleton
		self.window = window  # Store the window object where the skeleton will be drawn

	def move(self):
		# Move the skeleton randomly within a specified range
		self.position[0] += helpers.randint(-15, 15)  # Move horizontally
		self.position[1] += helpers.randint(-15, 15)  # Move vertically

		# Ensure the skeleton stays within the bounds of the window
		self.position[0] = max(0, min(self.window.get_width() - self.image.get_width(), self.position[0]))  # Limit horizontal movement
		self.position[1] = max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))  # Limit vertical movement

	def draw(self):
		# Draw the skeleton image on the window at the current position
		self.window.blit(self.image, self.position)
