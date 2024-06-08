import copy
import sys
from typing import Optional
import pygame
import assets
import screen
import display
import enemy
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
    window: display.Display = display.Display()
    match (args[0]):
        case "mage":
            player_class = mage.Mage(
                window.window.get_width() // 2,
                window.window.get_height() // 2,
                "Player",
                0.15,
            )
        case "rogue":
            player_class = rogue.Rogue(
                window.window.get_width() // 2,
                window.window.get_height() // 2,
                "Player",
                0.15,
            )
        case "warrior":
            player_class = warrior.Warrior(
                window.window.get_width() // 2,
                window.window.get_height() // 2,
                "Player",
                0.15,
            )
    if player_class is not None:
        window.add_screen("game", create_game_screen(player_class))
        window.set_screen("game")


def move_player(args, kwargs) -> None:  # pylint: disable=unused-argument
    pass


def create_main_menu(
    width: int, window: display.Display, font: pygame.font.Font
) -> screen.Screen:
    bground = pygame.transform.scale(
        assets.get_asset("main_menu_background").surf,
        (window.window.get_width(), window.window.get_height()),
    )
    half_width: int = width // 2
    main_menu: screen.Screen = screen.Screen(bground)
    main_menu.ui[0] = [
        ui_element.UI_Element(
            assets.get_asset("white"),
            half_width,
            150,
            rect=pygame.Rect(half_width, 150, 150, 30),
            center=True,
        ),
        ui_element.UI_Element(
            assets.get_asset("white"),
            half_width,
            200,
            rect=pygame.Rect(half_width, 200, 150, 30),
            center=True,
        ),
        ui_element.UI_Element(
            assets.get_asset("white"),
            half_width,
            250,
            rect=pygame.Rect(half_width, 250, 150, 30),
            center=True,
        ),
    ]
    main_menu.ui.append(
        [
            ui_element.UI_Element(
                "Start Game", width // 2, 150, font, True, [255, 0, 0], center=True
            ),
            ui_element.UI_Element(
                "Settings", width // 2, 200, font, True, [0, 0, 0], center=True
            ),
            ui_element.UI_Element(
                "Exit", width // 2, 250, font, True, [0, 0, 0], center=True
            ),
        ]
    )
    main_menu.register_key("play", pygame.K_RETURN, pygame.KMOD_NONE, play)
    main_menu.register_click_listener(main_menu.ui[0][0].design, "play", play)
    main_menu.register_click_listener(main_menu.ui[0][1].design, "settings", settings)
    main_menu.register_click_listener(main_menu.ui[0][2].design, "exit", leave)
    return main_menu


def create_settings_menu(
    height: int, window: display.Display, font: pygame.font.Font
) -> screen.Screen:
    bground = pygame.transform.scale(
        assets.get_asset("main_menu_background").surf,
        (window.window.get_width(), window.window.get_height()),
    )
    settings_menu: screen.Screen = screen.Screen(bground)
    settings_menu.ui[0] = [
        ui_element.UI_Element(
            assets.get_asset("white"),
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
    width: int, window: display.Display, height: int, font: pygame.font.Font
) -> screen.Screen:
    bground: pygame.Surface = pygame.transform.scale(
        assets.get_asset("main_menu_background").surf,
        (window.window.get_width(), window.window.get_height()),
    )
    class_select_menu: screen.Screen = screen.Screen(bground)
    images: list[surf_rect.Surf_Rect] = [
        assets.get_asset("rogue_button"),
        assets.get_asset("mage_button"),
        assets.get_asset("warrior_button"),
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
    class_select_menu.ui[0].append(
        ui_element.UI_Element(
            assets.get_asset("white"),
            50,
            height - 80,
            rect=pygame.Rect(50, height - 80, 100, 30),
        )
    )
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


def create_game_screen(player_surf_rect: player.Player) -> screen.Screen:
    window: display.Display = display.Display()
    bground: surf_rect.Surf_Rect = assets.get_asset("dungeon_map")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    enemies: list[enemy.Enemy] = [
        zombie.Zombie(50, 50),
        zombie.Zombie(window.window.get_width() - 120, 50),
        zombie.Zombie(50, window.window.get_height() - 120),
        zombie.Zombie(
            window.window.get_width() - 120, window.window.get_height() - 120
        ),
    ]
    game_screen: screen.Screen = screen.Screen(bground.surf)
    game_screen.entities[0].append(player_surf_rect)
    for enemy_inst in enemies:
        game_screen.entities[0].append(enemy_inst)
    game_screen.register_key("move_w", pygame.K_w, pygame.KMOD_NONE, move_player)
    game_screen.register_key("move_a", pygame.K_a, pygame.KMOD_NONE, move_player)
    game_screen.register_key("move_s", pygame.K_s, pygame.KMOD_NONE, move_player)
    game_screen.register_key("move_d", pygame.K_d, pygame.KMOD_NONE, move_player)
    return game_screen


def init() -> None:
    width: int = 800
    height: int = 600
    window: display.Display = display.Display([width, height])
    font = pygame.font.Font(None, 36)
    window.add_screen("main_menu", create_main_menu(width, window, font))
    window.add_screen("settings_menu", create_settings_menu(height, window, font))
    window.add_screen(
        "class_select_menu", create_class_select_menu(width, window, height, font)
    )
    window.set_screen("main_menu")
    while True:
        window.handle_events()


if __name__ == "__main__":
    init()
