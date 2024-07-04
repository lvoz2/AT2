# import tracemalloc

# tracemalloc.start()

import math
import sys
from typing import Any, Optional

import pygame

import create_menu as cm
import display
import enemy
import entity
import mage
import player
import rogue
import warrior

# import time


def play(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_scene("class_select_menu")


def settings(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    window: display.Display = display.Display()
    window.set_scene("settings_menu")


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
        window.set_scene(options["args"])
    else:
        window.set_scene(options["args"][0])


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
        window.add_scene("game", cm.create_game_scene(player_class, move_player))
        window.set_scene("game")


def move_player(
    event: pygame.event.Event,  # pylint: disable=unused-argument
    options: dict[str, Any],  # pylint: disable=unused-argument
) -> None:  # pylint: disable=unused-argument
    speed: float = 3.5
    direction: list[int] = [0, 0]
    if pygame.K_w in event.key and pygame.K_s not in event.key:
        direction[1] = -1
    elif pygame.K_w not in event.key and pygame.K_s in event.key:
        direction[1] = 1
    if pygame.K_a in event.key and pygame.K_d not in event.key:
        direction[0] = -1
    elif pygame.K_a not in event.key and pygame.K_d in event.key:
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


def check_dists(player_entity: player.Player) -> None:
    window: display.Display = display.Display()
    for e in window.scenes["game"].visible_elements:
        if isinstance(e, entity.Entity):
            distance: float = player_entity.get_distance(e)
            if isinstance(e, enemy.Enemy) and distance <= 50.0:
                player_entity.attack(0, e, window.events.event_types["dmg_event"])
                e.attack(0, player_entity, window.events.event_types["dmg_event"])


def init() -> None:
    width: int = 800
    height: int = 600
    window: display.Display = display.Display(
        title="Kings Quest", dim=[width, height], key_press_initial_delay=20
    )
    pygame.font.init()
    font: pygame.font.Font = pygame.font.Font(None, 36)
    window.add_scene(
        "main_menu", cm.create_main_menu(width, window, font, play, settings, leave)
    )
    window.add_scene(
        "settings_menu", cm.create_settings_menu(height, window, font, back)
    )
    window.add_scene(
        "class_select_menu",
        cm.create_class_select_menu(width, window, height, font, back, select_class),
    )
    window.set_scene("main_menu", no_event=True)
    while True:
        try:
            window.handle_events()
        except KeyboardInterrupt as e:
            raise e
            # snapshot = tracemalloc.take_snapshot()
            # top_stats = top_stats = snapshot.statistics("lineno")
            # print("[ Top 500 ]")
            # for stat in top_stats[:500]:
            #     if str(stat)[:32] == "/home/mint/Documents/GitHub/AT2/":
            #         print(stat)
            # sys.exit()


if __name__ == "__main__":
    init()
