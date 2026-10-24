import pgzrun
import settings
from pgzero.rect import Rect
from pgzero.actor import Actor
from pgzero.music import _music 
from pgzero.builtins import keyboard, keys, music, sounds



from ui import Button
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT


back_to_main_menu_button = Rect((WIDTH // 2 - 100, HEIGHT // 2 + 45), (200, 50))

active_screen = "start_screen"

start_button = Button("Start", (WIDTH // 2, 380), "green")
sound_button = Button("Sound: On", (WIDTH // 2, 450), "blue")
exit_button = Button("Exit", (WIDTH // 2, 520), "red")
back_to_game_button = Button("Back to Game", (WIDTH // 2, HEIGHT // 2 - 25), "green")
back_to_main_menu_button = Button("Main Menu", (WIDTH // 2, HEIGHT // 2 + 45), "red")

sound_on = True  

#* ================SOUND======================

def play_sound(name):
    if sound_on:
        getattr(sounds, name).play()
        
def toggle_sound():
    global sound_on
    sound_on = not sound_on
    play_sound("click")
    if sound_on:
        _music.unpause()
    else:
        _music.pause()
    sound_button.text = "Sound: On" if sound_on else "Sound: Off"

#*===================================================


def draw_pause_screen():
    screen.fill((0, 20, 0))

    screen.draw.text("Pause Screen", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Press ESC to return to the game", center=(WIDTH // 2, HEIGHT // 2 - 60), color="gray", fontsize=20)

    back_to_game_button.draw(screen)
    back_to_main_menu_button.draw(screen)


def draw_start_screen():
    screen.fill((0, 0, 0))

    screen.draw.text("Welcome Champ!!", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Let's play the game! Click the button", center=(WIDTH // 2, HEIGHT // 2 - 70), color="gray", fontsize=20)
    start_button.draw(screen)
    sound_button.draw(screen)
    exit_button.draw(screen)



def draw_game_screen():
    screen.fill((0, 0, 0))
    screen.draw.text("Game Screen", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=30)




def draw():
    SCREENS[active_screen]()


SCREENS = {
    "start_screen": draw_start_screen,
    "game_screen": draw_game_screen,
    "pause_screen": draw_pause_screen,
}

def update():
    pass

def exit():
    pgzrun.quit()



def on_mouse_down(pos):
    global active_screen

    if active_screen == "start_screen" and start_button.is_clicked(pos):
        play_sound("click")
        active_screen = "game_screen"
    elif active_screen == "start_screen" and sound_button.is_clicked(pos):
        toggle_sound()
    elif active_screen == "start_screen" and exit_button.is_clicked(pos):
        exit()

    elif active_screen == "pause_screen":
        play_sound("click")
        if back_to_game_button.is_clicked(pos):
            active_screen = "game_screen"

        elif back_to_main_menu_button.is_clicked(pos):
            play_sound("click")
            active_screen = "start_screen"


def on_key_down(key):
    global active_screen

    if key == keys.ESCAPE:
        if active_screen == "game_screen":
            active_screen = "pause_screen"
        elif active_screen == "pause_screen":
            active_screen = "game_screen"

music.set_volume(0.4)
music.play("dungeon")

pgzrun.go()
