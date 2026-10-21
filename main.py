import pgzrun
import Settings
from pgzero.rect import Rect
from pgzero.builtins import keyboard, keys
from pgzero.actor import Actor

WIDTH = Settings.WIDTH
HEIGHT = Settings.HEIGHT


start_buton = Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 50))
back_to_game_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 - 25), (200, 50))
back_to_main_menu_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 45), (200, 50))

active_screen = "start_screen"



def draw_button(rect, text, color, fontsize=25):
    screen.draw.filled_rect(rect, color)
    screen.draw.rect(rect, "white")
    screen.draw.text(text, center=rect.center, color="white", fontsize=fontsize)


def draw_pause_screen():
    screen.fill((0, 20, 0))

    screen.draw.text("Pause Screen", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Press ESC to return to the game", center=(WIDTH // 2, HEIGHT // 2 - 60), color="gray", fontsize=20)

    draw_button(back_to_game_button, "Back to Game", "green")
    draw_button(back_to_main_menu_button, "Main Menu", "red")


def draw_start_screen():
    screen.fill((0, 0, 0))

    screen.draw.text("Welcome Champ!!", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Let's play the game! Click the button", center=(WIDTH // 2, HEIGHT // 2 - 50), color="gray", fontsize=20)

    draw_button(start_buton, "Start", "green", fontsize=30)


def draw_game_screen():
    screen.fill((0, 0, 0))
    screen.draw.text("Game Screen", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=30)


SCREENS = {
    "start_screen": draw_start_screen,
    "game_screen": draw_game_screen,
    "pause_screen": draw_pause_screen,
}


def draw():
    SCREENS[active_screen]()


def update():
    pass


def on_mouse_down(pos):
    global active_screen

    if active_screen == "start_screen" and start_buton.collidepoint(pos):
        active_screen = "game_screen"

    elif active_screen == "pause_screen":
        if back_to_game_button.collidepoint(pos):
            active_screen = "game_screen"

        elif back_to_main_menu_button.collidepoint(pos):
            active_screen = "start_screen"


def on_key_down(key):
    global active_screen

    if key == keys.ESCAPE:
        if active_screen == "game_screen":
            active_screen = "pause_screen"
        elif active_screen == "pause_screen":
            active_screen = "game_screen"


pgzrun.go()
