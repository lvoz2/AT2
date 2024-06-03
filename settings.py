import pygame


class Settings:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.Font(None, 36)
        self.options = ["Volume", "Graphics", "Back"]
        self.selected_option = 0

    def run(self):
        running = True
        while running:
            self.window.fill((0, 0, 0))
            for index, option in enumerate(self.options):
                color = (255, 0, 0) if index == self.selected_option else (255, 255, 255)
                text = self.font.render(option, 1, color)
                self.window.blit(text, (50, 50 + index * 40))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=no-else-return
                    return 'quit'
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected_option] == "Back":
                            return 'back'
                        # Placeholder for setting adjustment functionality
                        print(f"Adjusting {self.options[self.selected_option]}")
                else:
                    pass

            return None
