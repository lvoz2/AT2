import pygame
from assets import GAME_ASSETS


class MainMenu:
	def __init__(self, window):
	self.window = window
	self.font = pygame.font.Font(None, 36)	# Specify the font size and style
	self.menu_options = ['Start Game', 'Settings', 'Exit']
	self.selected_option = 0	# The index of the currently selected menu option
	self.background_image = GAME_ASSETS['main_menu_background']	# Load the background image
	# Scale the background image to match the window size
	self.scaled_background = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))

	def run(self):
	"""Handles the display and interaction logic for the main menu."""
	running = True
	while running:
	# Blit the scaled background image to fill the entire window
	self.window.blit(self.scaled_background, (0, 0))

	# Display each menu option on the screen
	for index, option in enumerate(self.menu_options):
	# Highlight the selected option in red
	color = (255, 0, 0) if index == self.selected_option else (255, 255, 255)
	text = self.font.render(option, True, color)
	# Adjust the positioning of the text to be centered horizontally and slightly offset vertically
	text_rect = text.get_rect(center=(self.window.get_width() / 2, 150 + 50 * index))
	self.window.blit(text, text_rect)

	pygame.display.flip()	# Update the display with the new frame

	# Event handling in the menu
	for event in pygame.event.get():
	if event.type == pygame.QUIT:
	return 'quit'	# Return 'quit' if the window is closed
	elif event.type == pygame.KEYDOWN:
	if event.key == pygame.K_DOWN:
	self.selected_option = (self.selected_option + 1) % len(self.menu_options)
	elif event.key == pygame.K_UP:
	self.selected_option = (self.selected_option - 1) % len(self.menu_options)
	elif event.key == pygame.K_RETURN:
	# Return the current selected option when Enter is pressed
	return self.menu_options[self.selected_option]

	return 'quit'	# Default return value if the loop ends
