import copy
import math
import sys
from typing import Any, Optional

import pygame

import display
import enemy
import mage
import player
import rogue
import scene
import sprite
import ui_element
import warrior
import zombie


def play(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_screen("class_select_menu")


def settings(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_screen("settings_menu")


def leave(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    if not pygame.event.post(pygame.event.Event(pygame.QUIT)):
        sys.exit()


def back(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    if isinstance(options["args"], str):
        window.set_screen(options["args"])
    else:
        window.set_screen(options["args"][0])


def select_class(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    player_class: Optional[player.Player] = None
    window: display.Display = display.Display()
    match (options["args"]):
        case "mage":
            player_class = mage.Mage(
                rect_options={
                    "x": window.window.get_width() // 2,
                    "y": window.window.get_height() // 2,
                    "center": True,
                },
                name="Player",
                scale=0.3,
            )
        case "rogue":
            player_class = rogue.Rogue(
                rect_options={
                    "x": window.window.get_width() // 2,
                    "y": window.window.get_height() // 2,
                    "center": True,
                },
                name="Player",
                scale=0.3,
            )
        case "warrior":
            player_class = warrior.Warrior(
                rect_options={
                    "x": window.window.get_width() // 2,
                    "y": window.window.get_height() // 2,
                    "center": True,
                },
                name="Player",
                scale=0.3,
            )
    if player_class is not None:
        window.add_screen("game", create_game_screen(player_class))
        window.set_screen("game")


def move_player(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    speed: float = 2.0
    updated_state: Optional[bool] = None
    match (options["args"][0]):
        case "up":
            updated_state = False
        case "down":
            updated_state = True
        case _:
            raise ValueError('The arguments given in options were not "up" or "down"')
    move_key_state[event.key] = updated_state
    direction: list[int] = [0, 0]
    if move_key_state[pygame.K_w] and not move_key_state[pygame.K_s]:
        direction[1] = -1
    elif not move_key_state[pygame.K_w] and move_key_state[pygame.K_s]:
        direction[1] = 1
    if move_key_state[pygame.K_a] and not move_key_state[pygame.K_d]:
        direction[0] = -1
    elif not move_key_state[pygame.K_a] and move_key_state[pygame.K_d]:
        direction[0] = 1
    distance: float = math.sqrt((speed**2) * 2)
    match (direction):
        case [0, -1]:
            options["args"][1].move(0.0, distance)
        case [1, -1]:
            options["args"][1].move(45.0, distance)
        case [1, 0]:
            options["args"][1].move(90.0, distance)
        case [1, 1]:
            options["args"][1].move(135.0, distance)
        case [0, 1]:
            options["args"][1].move(180.0, distance)
        case [-1, 1]:
            options["args"][1].move(225.0, distance)
        case [-1, 0]:
            options["args"][1].move(270.0, distance)
        case [-1, -1]:
            options["args"][1].move(315.0, distance)


move_key_state: dict[int, bool] = {
    pygame.K_w: False,
    pygame.K_a: False,
    pygame.K_s: False,
    pygame.K_d: False,
}


def create_main_menu(
    width: int, window: display.Display, font: pygame.font.Font
) -> scene.Scene:
    bground: sprite.Sprite = window.get_asset("assets/main_menu_background.png")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    bground.rect.width = window.window.get_width()
    bground.rect.height = window.window.get_height()
    half_width: float = width / 2
    main_menu: scene.Scene = scene.Scene(bground)
    main_menu.elements[0] = [
        ui_element.UI_Element(
            sprite.Sprite(
                rect=pygame.Rect(half_width, 150, 150, 30),
                rect_options={
                    "center": True,
                    "x": half_width,
                    "y": 150,
                    "colour": [255, 255, 255],
                },
            ),
        ),
        ui_element.UI_Element(
            sprite.Sprite(
                rect=pygame.Rect(half_width, 200, 150, 30),
                rect_options={
                    "center": True,
                    "x": half_width,
                    "y": 200,
                    "colour": [255, 255, 255],
                },
            ),
        ),
        ui_element.UI_Element(
            sprite.Sprite(
                rect=pygame.Rect(half_width, 250, 150, 30),
                rect_options={
                    "center": True,
                    "x": half_width,
                    "y": 250,
                    "colour": [255, 255, 255],
                },
            ),
        ),
    ]
    main_menu.elements.append(
        [
            ui_element.UI_Element(
                sprite.Sprite(
                    rect_options={"x": half_width, "y": 150.0, "center": True},
                    font_options={
                        "text": "Start Game",
                        "font": font,
                        "colour": [255, 0, 0],
                    },
                )
            ),
            ui_element.UI_Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 200.0},
                    font_options={"text": "Settings", "font": font},
                ),
            ),
            ui_element.UI_Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 250.0},
                    font_options={"text": "Exit", "font": font},
                ),
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
    bground: sprite.Sprite = window.get_asset("assets/main_menu_background.png")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    settings_menu: scene.Scene = scene.Scene(bground)
    settings_menu.elements[0] = [
        ui_element.UI_Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 80, "colour": [255, 255, 255]},
            ),
        )
    ]
    settings_menu.elements.append(
        [
            ui_element.UI_Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": 100, "y": height - 65},
                    font_options={"text": "Back", "font": font},
                ),
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
    bground: sprite.Sprite = window.get_asset("assets/main_menu_background.png")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    class_select_menu: scene.Scene = scene.Scene(bground)
    images: list[str] = [
        "assets/rogue_button.png",
        "assets/mage_button.png",
        "assets/warrior_button.png",
    ]
    total_spacing = 20
    icon_width: int = ((width - total_spacing) // len(images)) - total_spacing
    for img_path in images:
        aspect_ratio: float = 0.75
        icon_height: int = int(icon_width // aspect_ratio)
        img: sprite.Sprite = window.get_asset(
            img_path,
            rect_options={
                "x": total_spacing
                + ((total_spacing + icon_width) * images.index(img_path)),
                "y": height // 3 - (height // 4) // 2,
            },
        )
        img.surf = pygame.transform.scale(img.surf, (icon_width, icon_height))
        class_select_menu.elements[0].append(ui_element.UI_Element(img))
    class_select_menu.elements[0].append(
        ui_element.UI_Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 80, "colour": [255, 255, 255]},
            ),
        )
    )
    class_select_menu.elements.append(
        [
            ui_element.UI_Element(
                sprite.Sprite(
                    rect_options={"x": 100, "y": height - 65, "center": True},
                    font_options={"text": "Back", "font": font},
                ),
            )
        ]
    )
    class_select_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "mage"}
    )
    class_select_menu.elements[0][1].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "rogue"}
    )
    class_select_menu.elements[0][2].register_listener(
        pygame.MOUSEBUTTONDOWN, select_class, {"args": "warrior"}
    )
    class_select_menu.elements[0][3].register_listener(
        pygame.MOUSEBUTTONDOWN, back, {"args": "main_menu"}
    )
    return class_select_menu


def create_game_screen(player_sprite: player.Player) -> scene.Scene:
    window: display.Display = display.Display()
    bground: sprite.Sprite = window.get_asset("assets/dungeon_map.png")
    bground.surf = pygame.transform.scale(
        bground.surf, (window.window.get_width(), window.window.get_height())
    )
    enemy_rect_options: list[dict[str, int]] = [
        {"x": 50, "y": 50},
        {"x": window.window.get_width() - 120, "y": 50},
        {"x": 50, "y": window.window.get_height() - 120},
        {
            "x": window.window.get_width() - 120,
            "y": window.window.get_height() - 120,
        },
    ]
    enemies: list[enemy.Enemy] = [
        zombie.Zombie(rect_options=rect_options) for rect_options in enemy_rect_options
    ]
    game_screen: scene.Scene = scene.Scene(bground)
    game_screen.elements[0].append(player_sprite)
    for enemy_inst in enemies:
        game_screen.elements[0].append(enemy_inst)
    game_screen.register_listener(
        pygame.KEYDOWN,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_w,
            "mods": pygame.KMOD_NONE,
            "args": ["down", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYDOWN,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_a,
            "mods": pygame.KMOD_NONE,
            "args": ["down", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYDOWN,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_s,
            "mods": pygame.KMOD_NONE,
            "args": ["down", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYDOWN,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_d,
            "mods": pygame.KMOD_NONE,
            "args": ["down", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYUP,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_w,
            "mods": pygame.KMOD_NONE,
            "args": ["up", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYUP,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_a,
            "mods": pygame.KMOD_NONE,
            "args": ["up", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYUP,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_s,
            "mods": pygame.KMOD_NONE,
            "args": ["up", player_sprite],
        },
    )
    game_screen.register_listener(
        pygame.KEYUP,
        lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
            event, options  # pylint: disable=unnecessary-lambda
        ),  # pylint: disable=unnecessary-lambda
        {
            "key": pygame.K_d,
            "mods": pygame.KMOD_NONE,
            "args": ["up", player_sprite],
        },
    )
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
