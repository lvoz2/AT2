import sys
from typing import Optional
import pygame
import assets
import screen
import display
import player
import mage
import rogue
import surf_rect
import warrior
import ui_element
import zombie


def play(args, kwargs) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_screen("class_select_menu")


def settings(args, kwargs) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_screen("settings_menu")


def leave(args, kwargs) -> None:  # pylint: disable=unused-argument
    if not pygame.event.post(pygame.event.Event(pygame.QUIT)):
        sys.exit()


def back(args, kwargs) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_screen(args[0])


def select_class(args, kwargs) -> None:  # pylint: disable=unused-argument
    player_class: Optional[player.Player] = None
    match (args[0]):
        case "mage":
            pass
        case "rogue":
            pass
        case "warrior":
            pass
    # window: display.Display = display.Display()
    # window.add_screen("game", create_game_screen())
    # window.set_screen("game")


def create_main_menu(
    width: int, window: display.Display, font: pygame.font.Font
) -> screen.Screen:
    bground = pygame.transform.scale(
        assets.GAME_ASSETS["main_menu_background"].surf,
        (window.window.get_width(), window.window.get_height()),
    )
    main_menu: screen.Screen = screen.Screen(bground)
    main_menu.ui[0] = [
        ui_element.UI_Element(
            "Start Game", width // 2, 150, font, True, [255, 0, 0], center=True
        ),
        ui_element.UI_Element(
            "Settings", width // 2, 200, font, True, [255, 0, 0], center=True
        ),
        ui_element.UI_Element(
            "Exit", width // 2, 250, font, True, [255, 0, 0], center=True
        ),
    ]
    main_menu.register_key("play", pygame.K_RETURN, pygame.KMOD_NONE, play)
    main_menu.register_click_listener(main_menu.ui[0][0].design, "play", play)
    main_menu.register_click_listener(main_menu.ui[0][1].design, "settings", settings)
    main_menu.register_click_listener(main_menu.ui[0][2].design, "exit", leave)
    return main_menu


def create_settings_menu(
    height: int, window: display.Display, font: pygame.font.Font
) -> screen.Screen:
    bground = pygame.transform.scale(
        assets.GAME_ASSETS["main_menu_background"].surf,
        (window.window.get_width(), window.window.get_height()),
    )
    settings_menu: screen.Screen = screen.Screen(bground)
    settings_menu.ui[0] = [
        ui_element.UI_Element(
            assets.GAME_ASSETS["white"],
            50,
            height - 80,
            rect=pygame.Rect(50, height - 80, 100, 30),
        )
    ]
    settings_menu.ui.append(
        [
            ui_element.UI_Element(
                "Back", 100, height - 65, font, True, [0, 0, 0], center=True
            )
        ]
    )
    settings_menu.register_click_listener(
        settings_menu.ui[0][0].design, "back", back, "main_menu"
    )
    return settings_menu


def create_class_select_menu(
    width: int, window: display.Display, height: int
) -> screen.Screen:
    bground: pygame.Surface = pygame.transform.scale(
        assets.GAME_ASSETS["main_menu_background"].surf,
        (window.window.get_width(), window.window.get_height()),
    )
    class_select_menu: screen.Screen = screen.Screen(bground)
    images: list[surf_rect.Surf_Rect] = [
        assets.GAME_ASSETS["rogue_button"],
        assets.GAME_ASSETS["mage_button"],
        assets.GAME_ASSETS["warrior_button"],
    ]
    total_spacing = 20
    icon_width: int = ((width - total_spacing) // len(images)) - total_spacing
    for img in images:
        aspect_ratio: float = 0.75
        icon_height: int = int(icon_width // aspect_ratio)
        img.surf = pygame.transform.scale(img.surf, (icon_width, icon_height))
        class_select_menu.ui[0].append(
            ui_element.UI_Element(
                img,
                x=total_spacing + ((total_spacing + icon_width) * images.index(img)),
                y=height // 3 - (height // 4) // 2,
            )
        )
    class_select_menu.ui.append([
        ui_element.UI_Element(
            assets.GAME_ASSETS["white"],
            50,
            height - 80,
            rect=pygame.Rect(50, height - 80, 100, 30),
        )
    ])
    class_select_menu.ui.append(
        [
            ui_element.UI_Element(
                "Back", 100, height - 65, font, True, [0, 0, 0], center=True
            )
        ]
    )
    class_select_menu.register_click_listener(
        class_select_menu.ui[0][0].design, "mage", select_class, "mage"
    )
    class_select_menu.register_click_listener(
        class_select_menu.ui[0][1].design, "rogue", select_class, "rogue"
    )
    class_select_menu.register_click_listener(
        class_select_menu.ui[0][2].design, "warrior", select_class, "warrior"
    )
    class_select_menu.register_click_listener(
        class_select_menu.ui[0][3].design, "back", back, "main_menu"
    )
    return class_select_menu


# def create_game_screen() -> screen.Screen:
# return


def init() -> None:
    width: int = 800
    height: int = 600
    window: display.Display = display.Display([width, height])
    font = pygame.font.Font(None, 36)
    window.add_screen("main_menu", create_main_menu(width, window, font))
    window.add_screen("settings_menu", create_settings_menu(height, window, font))
    window.add_screen(
        "class_select_menu", create_class_select_menu(width, window, height)
    )
    window.set_screen("settings_menu")
    while True:
        window.handle_events()


if __name__ == "__main__":
    init()
