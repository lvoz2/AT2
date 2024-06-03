import pygame
import screen


class Display:
    _instance = None

    def __new__(cls, cur_screen: str, scr: screen.Screen) -> None:
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Logger, cls).__new__(cls)
            self.screens: dict[str, screen.Screen] = {cur_screen: scr}
		    self.cur_screen = cur_screen
            pygame.init()
            self.window = pygame.display.set_mode((800, 600))
        return cls._instance
    
    @setter
    def set_screen(self, new_screen: str) -> None:
        if new_screen in self.screens.keys():
            self.cur_screen = new_screen
        else:
            raise KeyError("Screen not found, either because it does not exist or hasn't been loaded into the Display")
    
    def draw(self) -> None:
        pass