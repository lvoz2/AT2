import assets
import screen
import display
import player
import mage
import rogue
import warrior
import ui_element
# import zombie
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


def back(args, kwargs) -> None:
    window: display.Display = display.Display()
    window.set_screen(args[0])


def select_class(args, kwargs) -> None:
    player_class: Optional[player.Player] = None
    match (args[0]):
        case: "mage":
            pass
        case: "mage":
            pass
        case: "mage":
            pass
    window: display.Display = display.Display()
    window.add_screen("game", create_game_screen())
    window.set_screen("game")


def create_main_menu(width: int, height: int, window: display.Display, font: pygame.font.Font) -> screen.Screen:
    main_menu: screen.Screen = screen.Screen(assets.GAME_ASSETS["main_menu_background"])
    main_menu.ui[0] = [
        ui_element.UI_Element("Start Game", width / 2, 150, font, True, [255, 0, 0], center = True),
        ui_element.UI_Element("Settings", width / 2, 200, font, True, [255, 0, 0], center = True),
        ui_element.UI_Element("Exit", width / 2, 250, font, True, [255, 0, 0], center = True)
    ]
    main_menu.register_key("play", pygame.K_RETURN, pygame.KMOD_NONE, play)
    main_menu.register_click_listener(main_menu.ui[0][0], "play", play)
    main_menu.register_click_listener(main_menu.ui[0][1], "settings", settings)
    main_menu.register_click_listener(main_menu.ui[0][2], "exit", exit)
    return main_menu


def create_settings_menu(width: int, height: int, window: display.Display, font: pygame.font.Font) -> screen.Screen:
    settings_menu: screen.Screen = screen.Screen(assets.GAME_ASSETS["main_menu_background"])
    settings_menu.ui[0] = [
        ui_element.UI_Element(assets["white"], None, None, rect = pygame.Rect(50, height - 80, 100, 30))
    ]
    settings_menu.ui.append([
        ui_element.UI_Element("Back", 50, height - 80, font, True, [0, 0, 0])
    ])
    settings_menu.register_click_listener(settings_menu.ui[1][0], "back", back, "main_menu")
    return settings_menu


def create_class_select_menu(width: int, height: int, window: display.Display, font: pygame.font.Font) -> screen.Screen:
    class_select_menu: screen.Screen = screen.Screen(assets.GAME_ASSETS["main_menu_background"])
    images = [
        assets.GAME_ASSETS["mage"],
        assets.GAME_ASSETS["rogue_button"],
        assets.GAME_ASSETS["warrior_button"]
    ]
    total_spacing = 50
    scale = min(int(width - total_spacing * (len(images) + 1) // len(images) * images[0].get_height() / images[0].get_width()), height) / images[0].get_height()
    class_select_menu.ui[0] = [
        ui_element.UI_Element(
            images[i],
            total_spacing + (images[i].get_width() * scale * i),
            images[i].get_height() * scale, 
            scale
        ) for i in range(len(images))
    ]
    class_select_menu.register_click_listener(class_select_menu.ui[0][0], "mage", select_class, "mage")
    class_select_menu.register_click_listener(class_select_menu.ui[0][1], "rogue", select_class, "rogue")
    class_select_menu.register_click_listener(class_select_menu.ui[0][2], "warrior", select_class, "warrior")
    return class_select_menu


def create_game_screen() -> Optional[screen.Screen]:
    return None


if __name__ == "__main__":
    width: int = 800
    height: int = 600
    window: display.Display = display.Display([width, height])
    font = pygame.font.Font(None, 36)
    window.add_screen("main_menu", create_main_menu(width, height, window, font))
    window.add_screen("settings_menu", create_settings_menu(width, height, window, font))
    window.add_screen("class_select_menu", create_class_select_menu(width, height, window, font))
    window.set_screen("main_menu")
