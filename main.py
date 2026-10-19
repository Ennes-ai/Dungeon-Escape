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
pause_screen_active = False



def draw_pause_screen():
    screen.fill((0, 20, 0))
    
    screen.draw.text("Pause Screen", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Press ESC to return to the game", center=(WIDTH // 2, HEIGHT // 2 - 60), color="gray", fontsize=20)
    
  
    screen.draw.filled_rect(back_to_game_button, "green")
    screen.draw.rect(back_to_game_button, "white") 
    screen.draw.text("Back to Game", center=back_to_game_button.center, color="white", fontsize=25)
    
   
    screen.draw.filled_rect(back_to_main_menu_button, "red")
    screen.draw.rect(back_to_main_menu_button, "white")
    screen.draw.text("Main Menu", center=back_to_main_menu_button.center, color="white", fontsize=25)


def draw_start_screen():
    screen.fill((0, 0, 0))
    
    screen.draw.text("Welcome Champ!!", center=(WIDTH // 2, HEIGHT // 2 - 100), color="white", fontsize=40)
    screen.draw.text("Let's play the game! Click the button", center=(WIDTH // 2, HEIGHT // 2 - 50), color="gray", fontsize=20)
    
   
    screen.draw.filled_rect(start_buton, "green")
    screen.draw.rect(start_buton, "white")
    

    
    screen.draw.text("Start", center=start_buton.center, color="white", fontsize=30)


def draw_game_screen():
    screen.fill((0, 0, 0))
    screen.draw.text("Game Screen", center=(WIDTH // 2, HEIGHT // 2), color="white", fontsize=30)


def draw():
    
    if active_screen == "start_screen":
        draw_start_screen()
    elif active_screen == "game_screen":
        draw_game_screen()
    elif active_screen == "pause_screen":
        draw_pause_screen() 


def update():
    pass 


def on_mouse_down(pos):
    global active_screen, pause_screen_active 
    
    
    if active_screen == "start_screen" and start_buton.collidepoint(pos):
        active_screen = "game_screen"
        
  
    elif active_screen == "pause_screen":
        if back_to_game_button.collidepoint(pos):
            active_screen = "game_screen"
            pause_screen_active = False
            
        elif back_to_main_menu_button.collidepoint(pos):
            active_screen = "start_screen"
            pause_screen_active = False


def on_key_down(key):
    global active_screen, pause_screen_active
    
    if key == keys.ESCAPE and active_screen == "game_screen":
        pause_screen_active = True
        active_screen = "pause_screen"
        
    elif key == keys.ESCAPE and active_screen == "pause_screen":
        pause_screen_active = False
        active_screen = "game_screen"


pgzrun.go()