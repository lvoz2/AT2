from typing import Any, Callable

import pygame

import display
import element
import enemy
import healthbar
import player
import scene
import sprite
import utils
import zombie

bgrounds: dict[str, sprite.Sprite] = {}


def create_main_menu(
    width: int,
    window: display.Display | display.AsyncDisplay,
    font: pygame.font.Font,
    play: Callable[[pygame.event.Event, dict[str, Any]], None],
    settings: Callable[[pygame.event.Event, dict[str, Any]], None],
    leave: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.rect.width = window.dimensions[0]
        bground.rect.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/main_menu_background.png"]
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
                    is_async=window.from_async,
                    executor=window.executor,
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
                    is_async=window.from_async,
                    executor=window.executor,
                ),
                visible=True,
            ),
            element.Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 200.0},
                    font_options={"text": "Settings", "font": font},
                    is_async=window.from_async,
                    executor=window.executor,
                ),
                visible=True,
            ),
            element.Element(
                sprite.Sprite(
                    rect_options={"center": True, "x": half_width, "y": 250.0},
                    font_options={"text": "Exit", "font": font},
                    is_async=window.from_async,
                    executor=window.executor,
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
    height: int,
    window: display.Display | display.AsyncDisplay,
    font: pygame.font.Font,
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.rect.width = window.dimensions[0]
        bground.rect.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/main_menu_background.png"]
    settings_menu: scene.Scene = scene.Scene(bground)
    settings_menu.elements[0] = [
        element.Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 80, "colour": [255, 255, 255]},
                is_async=window.from_async,
                executor=window.executor,
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
                    is_async=window.from_async,
                    executor=window.executor,
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
    width: int,
    window: display.Display | display.AsyncDisplay,
    height: int,
    font: pygame.font.Font,
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
    select_class: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.rect.width = window.dimensions[0]
        bground.rect.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/main_menu_background.png"]
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
        img: sprite.Sprite = utils.get_asset(
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
                is_async=window.from_async,
                executor=window.executor,
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
                    is_async=window.from_async,
                    executor=window.executor,
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


def create_game_scene(
    player_sprite: player.Player,
    move_player: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    window: display.Display = display.Display()
    if "assets/dungeon_map.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/dungeon_map.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.rect.width = window.dimensions[0]
        bground.rect.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/dungeon_map.png"]
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
    game_scene: scene.Scene = scene.Scene(bground)
    game_scene.elements[0].append(player_sprite)
    for enemy_inst in enemies:
        game_scene.elements[0].append(enemy_inst)
    player_hp_bar_bground = element.Element(
        sprite.Sprite(
            rect=pygame.Rect(10, 10, 260, 30),
            rect_options={"x": 10, "y": 10, "colour": [192, 192, 192]},
            is_async=window.from_async,
            executor=window.executor,
        ),
        visible=True,
    )
    player_hp_bar = healthbar.HealthBar(
        player_sprite.health,
        pygame.Rect(15, 15, 250, 20),
        {"x": 15, "y": 15, "colour": [255, 0, 0]},
    )
    player_sprite.register_listener(
        window.events.event_types["dmg_event"],
        lambda event, options: player_hp_bar.update(event.target.health),
    )
    game_scene.elements[0].append(player_hp_bar_bground)
    game_scene.elements.append([player_hp_bar])
    keys: list[int] = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]
    game_scene.register_listener(
        "key_press",
        move_player,
        {
            "key": keys,
            "mods": [pygame.KMOD_NONE],
            "args": player_sprite,
        },
    )
    return game_scene


def create_attack_scene() -> scene.Scene:
    window: display.Display = display.Display()
    if "assets/attack_screen.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/attack_screen.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.rect.width = window.dimensions[0]
        bground.rect.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/attack_screen.png"]
    attack_scene: scene.Scene = scene.Scene(bground)
    return attack_scene
