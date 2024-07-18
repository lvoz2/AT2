import functools
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
import skeleton

pygame.font.init()
bgrounds: dict[str, sprite.Sprite] = {}
game_fonts: list[pygame.font.Font] = [
    pygame.font.Font(None, 36),
    pygame.font.Font(None, 20),
]


def create_main_menu(
    width: int,
    height: int,
    window: display.Display | display.AsyncDisplay,
    play: Callable[[pygame.event.Event, dict[str, Any]], None],
    settings: Callable[[pygame.event.Event, dict[str, Any]], None],
    leave: Callable[[pygame.event.Event, dict[str, Any]], None],
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
    select_class: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    font = game_fonts[0]
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.width = window.dimensions[0]
        bground.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/main_menu_background.png"]
    half_width: float = width / 2
    main_menu: scene.Scene = scene.Scene(bground)
    y_vals: list[int] = [152, 205, 252]
    for y_val in y_vals:
        main_menu.elements[0].append(
            element.Element(
                sprite.Sprite(
                    rect=pygame.Rect(half_width, y_val, 150, 40),
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
    main_menu.elements[0][0].register_listener(
        pygame.MOUSEBUTTONDOWN,
        play,
        {"args": [width, window, height, back, select_class]},
    )
    main_menu.elements[0][1].register_listener(
        pygame.MOUSEBUTTONDOWN, settings, {"args": [height, window, back]}
    )
    main_menu.elements[0][2].register_listener(pygame.MOUSEBUTTONDOWN, leave)
    return main_menu


def create_settings_menu(
    height: int,
    window: display.Display | display.AsyncDisplay,
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    font = game_fonts[0]
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.width = window.dimensions[0]
        bground.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/main_menu_background.png"]
    settings_menu: scene.Scene = scene.Scene(bground)
    settings_menu.elements[0] = [
        element.Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 80, 100, 30),
                rect_options={"x": 50, "y": height - 78, "colour": [255, 255, 255]},
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


def create_class_select_menu(  # pylint: disable=too-many-locals
    width: int,
    window: display.Display | display.AsyncDisplay,
    height: int,
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
    select_class: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    font = game_fonts[0]
    if "assets/main_menu_background.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/main_menu_background.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.width = window.dimensions[0]
        bground.height = window.dimensions[1]
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
        img.width, img.height = icon_width, icon_height
        class_select_menu.elements[0].append(element.Element(img, visible=True))
    class_select_menu.elements[0].append(
        element.Element(
            sprite.Sprite(
                rect=pygame.Rect(50, height - 50, 100, 30),
                rect_options={"x": 50, "y": height - 78, "colour": [255, 255, 255]},
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
        bground.width = window.dimensions[0]
        bground.height = window.dimensions[1]
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
        skeleton.Skeleton(rect_options=rect_options)
        for rect_options in enemy_rect_options
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


def create_attack_scene(  # pylint: disable=too-many-locals
    player_entity: player.Player,
    target: enemy.Enemy,
    back: Callable[[pygame.event.Event, dict[str, Any]], None],
) -> scene.Scene:
    title_font = game_fonts[0]
    text_font = game_fonts[1]
    window: display.Display = display.Display()
    if "assets/attack_screen.png" not in bgrounds:
        bground: sprite.Sprite = utils.get_asset("assets/attack_screen.png")
        bground.surf = pygame.transform.scale(
            bground.surf, (window.dimensions[0], window.dimensions[1])
        )
        bground.width = window.dimensions[0]
        bground.height = window.dimensions[1]
    else:
        bground = bgrounds["assets/attack_screen.png"]
    attack_scene: scene.Scene = scene.Scene(bground)
    player_rect = player_entity.design.rect.copy()
    player_scale = 150 / min(player_rect.width, player_rect.height)
    player_e = element.Element(
        sprite.Sprite(
            player_entity.design.surf,
            player_rect,
            scale=player_scale,
            path=player_entity.design.path,
            is_async=window.from_async,
            executor=window.executor,
        )
    )
    new_player_rect = player_e.design.rect.copy()
    new_player_rect.centerx = 200
    new_player_rect.bottom = 300
    player_e.design.rect = new_player_rect
    target_rect = target.design.rect.copy()
    target_scale = 150 / min(target_rect.width, target_rect.height)
    target_e = element.Element(
        sprite.Sprite(
            target.design.surf,
            target_rect,
            scale=target_scale,
            path=target.design.path,
            is_async=window.from_async,
            executor=window.executor,
        )
    )
    new_target_rect = target_e.design.rect.copy()
    new_target_rect.centerx = 600
    new_target_rect.bottom = 200
    target_e.design.rect = new_target_rect
    left_panel_title: element.Element = element.Element(
        sprite.Sprite(
            rect_options={"center": True, "x": 200, "y": 342},
            font_options={"text": "~ ATTACKS ~", "font": title_font},
            is_async=window.from_async,
            executor=window.executor,
        ),
        visible=True,
    )
    right_panel_title: element.Element = element.Element(
        sprite.Sprite(
            rect_options={"center": True, "x": 600, "y": 342},
            font_options={"text": "~ OTHER ~", "font": title_font},
            is_async=window.from_async,
            executor=window.executor,
        ),
        visible=True,
    )
    leave_text: element.Element = element.Element(
        sprite.Sprite(
            rect_options={"x": 400, "y": 558, "center": True},
            font_options={"text": "~ RUN ~", "font": title_font},
            is_async=window.from_async,
            executor=window.executor,
        ),
        visible=True,
    )
    leave_text_container: element.Element = element.Element(
        sprite.Sprite(
            rect=pygame.Rect(340, 540, 120, 36),
            rect_options={"colour": [209, 211, 212]},
        )
    )
    leave_text_container.register_listener("mouse_button_down", back, {"args": "game"})
    attack_scene.elements[0] = [
        player_e,
        target_e,
        left_panel_title,
        right_panel_title,
        leave_text_container,
        leave_text,
    ]
    attack_funcs: list[functools.partial[None]] = []
    # attack_menu_rect = pygame.Rect(45, 355, 340, 190)
    for i, (name, attack) in enumerate(player_entity.attacks):
        text: element.Element = element.Element(
            sprite.Sprite(
                rect_options={"x": 45, "y": 355 + (i * 30)},
                font_options={"text": name, "font": text_font},
                is_async=window.from_async,
                executor=window.executor,
            ),
            visible=True,
        )
        dmg: element.Element = element.Element(
            sprite.Sprite(
                rect_options={"x": 235, "y": 355 + (i * 30)},
                font_options={
                    "text": "DMG: " + str(int(attack.dmg * player_entity.strength)),
                    "font": text_font,
                },
                is_async=window.from_async,
                executor=window.executor,
            ),
            visible=True,
        )
        cost: element.Element = element.Element(
            sprite.Sprite(
                rect_options={"x": 310, "y": 355 + (i * 30)},
                font_options={"text": "Cost: " + str(attack.cost), "font": text_font},
                is_async=window.from_async,
                executor=window.executor,
            ),
            visible=True,
        )
        container: element.Element = element.Element(
            sprite.Sprite(
                rect=pygame.Rect(45, 355 + (i * 30), 340, 30),
                rect_options={"colour": [209, 211, 212]},
            )
        )
        attack_funcs.append(
            functools.partial(
                player_entity.attack,
                i,
                target,
                window.events.event_types["dmg_event"],
            )
        )
        container.register_listener(
            "mouse_button_down",
            lambda event, options: attack_funcs[options["i"]](),
            {"i": i},
        )
        attack_scene.elements[0].append(container)
        attack_scene.elements[0].append(text)
        attack_scene.elements[0].append(dmg)
        attack_scene.elements[0].append(cost)
    # other_menu_rect = pygame.Rect(445, 355, 340, 190)
    return attack_scene
