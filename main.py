import assets
import screen
import display
import mage
import rogue
import warrior
import ui_element
import zombie
import pygame
import sys


def play(args, kwargs) -> None:
    window: display.Display = display.Display()
    window.set_screen("class_select")


def settings(args, kwargs) -> None:
    window: display.Display = display.Display()
    window.set_screen("settings")


def exit(args, kwargs) -> None:
    if not pygame.event.post(pygame.QUIT):
        sys.exit()


if __name__ == "__main__":
    main_menu: screen.Screen = screen.Screen(assets.GAME_ASSETS["main_menu_background"])
    width: int = 800
    height: int = 600
    window: display.Display = display.Display([width, height])
    font = pygame.font.Font(None, 36)
    main_menu.ui[0] = [
        ui_element.UI_Element("Start Game", 400, 150, font, True, "#FF0000", center = True),
        ui_element.UI_Element("Settings", 400, 200, font, True, "#FF0000", center = True),
        ui_element.UI_Element("Exit", 400, 250, font, True, "#FF0000", center = True)
    ]
    main_menu.register_key("play", pygame.K_RETURN, pygame.KMOD_NONE, play)
    main_menu.register_click_listener(main_menu.ui[0][0], "play", play)
    main_menu.register_click_listener(main_menu.ui[0][1], "settings", settings)
    main_menu.register_click_listener(main_menu.ui[0][2], "exit", exit)
    window.add_screen(main_menu)
    # window.add_screen(settings_menu)
    # window.add_screen(class_select_menu)
