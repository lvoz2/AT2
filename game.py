import copy
import sys
from typing import Optional
import pygame
import assets
import scene
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
) -> scene.Scene:
    bground: surf_rect.Surf_Rect = assets.get_asset("main_menu_background")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    half_width: int = width // 2
    main_menu: scene.Scene = scene.Scene(bground)
    main_menu.elements[0] = [
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
    main_menu.elements.append(
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
    main_menu.register_listener(pygame.KEYDOWN, play, {"key": pygame.K_RETURN})
    main_menu.elements[0][0].register_listener(pygame.MOUSEBUTTONDOWN, play)
    main_menu.elements[0][1].register_listener(pygame.MOUSEBUTTONDOWN, settings)
    main_menu.elements[0][2].register_listener(pygame.MOUSEBUTTONDOWN, leave)
    return main_menu


def create_settings_menu(
    height: int, window: display.Display, font: pygame.font.Font
) -> scene.Scene:
    bground: surf_rect.Surf_Rect = assets.get_asset("main_menu_background")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    settings_menu: scene.Scene = scene.Scene(bground)
    settings_menu.elements[0] = [
        ui_element.UI_Element(
            assets.get_asset("white"),
            50,
            height - 80,
            rect=pygame.Rect(50, height - 80, 100, 30),
        )
    ]
    settings_menu.elements.append(
        [
            ui_element.UI_Element(
                "Back", 100, height - 65, font, True, [0, 0, 0], center=True
            )
        ]
    )
    settings_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, back, {"args": "main_menu"}
    )
    return settings_menu


def create_class_select_menu(
    width: int, window: display.Display, height: int, font: pygame.font.Font
) -> scene.Scene:
    bground: surf_rect.Surf_Rect = assets.get_asset("main_menu_background")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    class_select_menu: scene.Scene = scene.Scene(bground)
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
        class_select_menu.elements[0].append(
            ui_element.UI_Element(
                img,
                x=total_spacing + ((total_spacing + icon_width) * images.index(img)),
                y=height // 3 - (height // 4) // 2,
            )
        )
    class_select_menu.elements[0].append(
        ui_element.UI_Element(
            assets.get_asset("white"),
            50,
            height - 80,
            rect=pygame.Rect(50, height - 80, 100, 30),
        )
    )
    class_select_menu.elements.append(
        [
            ui_element.UI_Element(
                "Back", 100, height - 65, font, True, [0, 0, 0], center=True
            )
        ]
    )
    class_select_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "mage"}
    )
    class_select_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "rogue"}
    )
    class_select_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "warrior"}
    )
    class_select_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, back, {"args": "main_menu"}
    )
    return class_select_menu


def create_game_screen(player_surf_rect: player.Player) -> scene.Scene:
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
    game_screen: scene.Scene = scene.Scene(bground)
    game_screen.elements[0].append(player_surf_rect)
    for enemy_inst in enemies:
        game_screen.elements[0].append(enemy_inst)
    game_screen.register_listener(pygame.KEYDOWN, move_player, {"key": pygame.K_w, "mods": pygame.KMOD_NONE})
    game_screen.register_listener(pygame.KEYDOWN, move_player, {"key": pygame.K_a, "mods": pygame.KMOD_NONE})
    game_screen.register_listener(pygame.KEYDOWN, move_player, {"key": pygame.K_s, "mods": pygame.KMOD_NONE})
    game_screen.register_listener(pygame.KEYDOWN, move_player, {"key": pygame.K_d, "mods": pygame.KMOD_NONE})
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
