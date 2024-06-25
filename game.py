import copy
import math
import sys
from typing import Any, Callable, Optional

import pygame

import display
import element
import enemy
import entity
import healthbar
import mage
import player
import rogue
import scene
import sprite
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
    rect_options: dict[str, Any] = {
        "x": window.window.get_width() // 2,
        "y": window.window.get_height() // 2,
        "center": True,
    }
    match (options["args"]):
        case "mage":
            player_class = mage.Mage(
                rect_options=rect_options,
                name="Player",
                scale=0.3,
            )
        case "rogue":
            player_class = rogue.Rogue(
                rect_options=rect_options,
                name="Player",
                scale=0.3,
            )
        case "warrior":
            player_class = warrior.Warrior(
                rect_options=rect_options,
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
    match (event.type):
        case pygame.KEYUP:
            updated_state = False
        case pygame.KEYDOWN:
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
    distance: list[float] = [speed, math.sqrt((speed**2) * 2)]
    match (direction):
        case [0, -1]:
            options["args"].move(0.0, distance[0])
        case [1, -1]:
            options["args"].move(45.0, distance[1])
        case [1, 0]:
            options["args"].move(90.0, distance[0])
        case [1, 1]:
            options["args"].move(135.0, distance[1])
        case [0, 1]:
            options["args"].move(180.0, distance[0])
        case [-1, 1]:
            options["args"].move(225.0, distance[1])
        case [-1, 0]:
            options["args"].move(270.0, distance[0])
        case [-1, -1]:
            options["args"].move(315.0, distance[1])
    check_dists(options["args"])


move_key_state: dict[int, bool] = {
    pygame.K_w: False,
    pygame.K_a: False,
    pygame.K_s: False,
    pygame.K_d: False,
}


def check_dists(player_entity: player.Player) -> None:
    window: display.Display = display.Display()
    for e in window.screens["game"].visible_elements:
        if isinstance(e, entity.Entity):
            distance: float = player_entity.get_distance(e)
            if isinstance(e, enemy.Enemy) and distance <= 50.0:
                player_entity.attack(0, e, custom_events["dmg_event"])
                e.attack(0, player_entity, custom_events["dmg_event"])


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
    y_vals: list[int] = [150, 200, 250]
    for y_val in y_vals:
        main_menu.elements[0].append(
            element.Element(
                sprite.Sprite(
                    rect=pygame.Rect(half_width, y_val, 150, 30),
                    rect_options={
                        "center": True,
                        "x": half_width,
                        "y": y_val,
                        "colour": [255, 255, 255],
                    },
                ),
                visible=True,
            )
        )
    main_menu.elements.append(
        [
            element.Element(
                sprite.Sprite(
                    rect_options={"x": half_width, "y": 150.0, "center": True},
                    font_options={
                        "text": "Start Game",
                        "font": font,
                        "colour": [255, 0, 0],
                    },
                ),
                visible=True,
            ),
            element.Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 200.0},
                    font_options={"text": "Settings", "font": font},
                ),
                visible=True,
            ),
            element.Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 250.0},
                    font_options={"text": "Exit", "font": font},
                ),
                visible=True,
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
        element.Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 80, "colour": [255, 255, 255]},
            ),
            visible=True,
        )
    ]
    settings_menu.elements.append(
        [
            element.Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": 100, "y": height - 65},
                    font_options={"text": "Back", "font": font},
                ),
                visible=True,
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
        img.rect.width, img.rect.height = icon_width, icon_height
        class_select_menu.elements[0].append(element.Element(img, visible=True))
    class_select_menu.elements[0].append(
        element.Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 80, "colour": [255, 255, 255]},
            ),
            visible=True,
        )
    )
    class_select_menu.elements.append(
        [
            element.Element(
                sprite.Sprite(
                    rect_options={"x": 100, "y": height - 65, "center": True},
                    font_options={"text": "Back", "font": font},
                ),
                visible=True,
            )
        ]
    )
    for i, player_class in enumerate(["rogue", "mage", "warrior"]):
        class_select_menu.elements[0][i].register_listener(
            pygame.MOUSEBUTTONDOWN, select_class, {"args": player_class}
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
    player_hp_bar_bground = element.Element(
        sprite.Sprite(
            rect=pygame.Rect(10, 10, 260, 30),
            rect_options={"x": 10, "y": 10, "colour": [192, 192, 192]},
        ),
        visible=True,
    )
    player_hp_bar = healthbar.HealthBar(
        player_sprite.health,
        pygame.Rect(15, 15, 250, 20),
        {"x": 15, "y": 15, "colour": [255, 0, 0]},
    )
    player_sprite.register_listener(
        custom_events["dmg_event"],
        lambda event, options: player_hp_bar.update(event.target.health),
    )
    game_screen.elements[0].append(player_hp_bar_bground)
    game_screen.elements.append([player_hp_bar])
    keys: list[int] = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    for press_type in [pygame.KEYDOWN, pygame.KEYUP]:
        for key in keys:
            game_screen.register_listener(
                press_type,
                lambda event, options: move_player(  # pylint: disable=unnecessary-lambda
                    event, options  # pylint: disable=unnecessary-lambda
                ),  # pylint: disable=unnecessary-lambda
                {
                    "key": key,
                    "mods": pygame.KMOD_NONE,
                    "args": player_sprite,
                },
            )
    return game_screen


custom_events: dict[str, int] = {}


def process_dmg(
    event: pygame.event.Event,
    func: Callable[[pygame.event.Event, dict[str, Any]], None],
    options: Optional[dict[str, Any]],
) -> bool:
    if options is not None:
        if options["target"] == event.target:
            func(event, options)
            return True
    return False


def init() -> None:
    custom_events["dmg_event"] = pygame.event.custom_type()
    width: int = 800
    height: int = 600
    window: display.Display = display.Display("Kings Quest", [width, height])
    window.events.register_processor(custom_events["dmg_event"], process_dmg)
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
