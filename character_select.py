import pygame
from assets import GAME_ASSETS


class CharacterSelect:
	"""
	A class representing the character selection screen.

	Attributes:
		window (pygame.Surface): The game window surface.
		font (pygame.font.Font): The font used for text rendering.
		background_image (pygame.Surface): The background image of the character selection screen.
		characters (dict): A dictionary mapping character names to their corresponding button images.
		character_buttons (dict): A dictionary mapping character names to their button rectangles.
		back_button (pygame.Rect): The rectangle representing the back button.

	Methods:
		__init__(self, window): Initializes the CharacterSelect object.
		setup_character_buttons(self): Sets up the character buttons.
		run(self): Runs the character selection screen loop.
	"""

	def __init__(self, window):
		"""
		Initializes the CharacterSelect object.

		Args:
			window (pygame.Surface): The game window surface.
		"""
		self.window = window
		self.font = pygame.font.Font(None, 36)  # Use a default font
		self.background_image = GAME_ASSETS['main_menu_background'].convert()
		self.background_image = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
		self.characters = {
			"Warrior": GAME_ASSETS['warrior_button'].convert_alpha(),
			"Mage": GAME_ASSETS['mage_button'].convert_alpha(),
			"Rogue": GAME_ASSETS['rogue_button'].convert_alpha()
		}
		self.character_buttons = self.setup_character_buttons()
		self.back_button = pygame.Rect(50, self.window.get_height() - 50 - 30, 100, 30)  # Positioned at bottom left

	def setup_character_buttons(self):
		"""
		Sets up the character buttons.

		Returns:
			dict: A dictionary mapping character names to their button rectangles.
		"""
		buttons = {}
		total_spacing = 40  # spacing between buttons and edges
		num_buttons = len(self.characters)
		available_width = self.window.get_width() - total_spacing * (num_buttons + 1)
		button_width = available_width // num_buttons
		max_height = self.window.get_height() // 4  # maximum button height

		x = total_spacing
		y = self.window.get_height() // 3 - max_height // 2  # position them a bit higher to make space for back button

		for character, image in self.characters.items():
			aspect_ratio = image.get_height() / image.get_width()
			button_height = int(button_width * aspect_ratio)
			button_height = min(button_height, max_height)  # Ensure button isn't too tall
			scaled_image = pygame.transform.scale(image, (button_width, button_height))
			buttons[character] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
			x += button_width + total_spacing

		return buttons

	def run(self):
		self.window.blit(self.background_image, (0, 0))
		for character, (image, rect) in self.character_buttons.items():
			self.window.blit(image, rect)

		# Draw back button
		pygame.draw.rect(self.window, (200, 200, 200), self.back_button)  # Draw a grey button
		back_text = self.font.render('Back', True, (0, 0, 0))
		text_rect = back_text.get_rect(center=self.back_button.center)
		self.window.blit(back_text, text_rect)

		pygame.display.flip()
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return None
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if self.back_button.collidepoint(event.pos):
						return 'back'
					for character, (image, rect) in self.character_buttons.items():
						if rect.collidepoint(event.pos):
							return character

		return None
