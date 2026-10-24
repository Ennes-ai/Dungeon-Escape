import pgzrun
from pgzero.builtins import exit, keys, music, sounds
from pgzero.screen import Screen

import settings
from level import MAP, Level, cell_to_foot
from sprites import AnimatedSprite, Goblin, Hero, Skeleton
from ui import Button

TITLE = settings.TITLE
WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
CENTER_X = WIDTH // 2

screen: Screen

ENEMY_TYPES = {"g": Goblin, "s": Skeleton}
COIN_ANIMATION = {"idle": [f"coin_{i}" for i in range(4)]}

start_button = Button("Start", (CENTER_X, 380), "green")
sound_button = Button("Sound: On", (CENTER_X, 450), "blue")
exit_button = Button("Exit", (CENTER_X, 520), "red")
back_to_game_button = Button("Back to Game", (CENTER_X, HEIGHT // 2 - 25),
                             "green")
back_to_main_menu_button = Button("Main Menu", (CENTER_X, HEIGHT // 2 + 45),
                                  "red")
play_again_button = Button("Play Again", (CENTER_X, 430), "green")
end_menu_button = Button("Main Menu", (CENTER_X, 500), "red")

active_screen = "start_screen"
sound_on = True


def make_coin(col, row):
    x, y = cell_to_foot(col, row)
    return AnimatedSprite(COIN_ANIMATION, (x, y - 12))


def reset_game():
    global level, hero, enemies, coin_sprites
    level = Level(MAP)
    hero = Hero(*level.hero_start)
    enemies = [ENEMY_TYPES[char](col, row)
               for char, col, row in level.enemy_spawns]
    coin_sprites = {cell: make_coin(*cell) for cell in level.coins}


reset_game()


def play_sound(name):
    if sound_on:
        getattr(sounds, name).play()


def toggle_sound():
    global sound_on
    sound_on = not sound_on
    play_sound("click")
    if sound_on:
        music.unpause()
    else:
        music.pause()
    sound_button.text = "Sound: On" if sound_on else "Sound: Off"


def draw_pause_screen():
    screen.fill((0, 20, 0))
    screen.draw.text("Pause Screen", center=(CENTER_X, HEIGHT // 2 - 100),
                     color="white", fontsize=40)
    screen.draw.text("Press ESC to return to the game",
                     center=(CENTER_X, HEIGHT // 2 - 60),
                     color="gray", fontsize=20)
    back_to_game_button.draw(screen)
    back_to_main_menu_button.draw(screen)


def draw_start_screen():
    screen.fill((0, 0, 0))
    screen.draw.text("Welcome Champ!!", center=(CENTER_X, HEIGHT // 2 - 100),
                     color="white", fontsize=40)
    screen.draw.text("Let's play the game! Click the button",
                     center=(CENTER_X, HEIGHT // 2 - 70),
                     color="gray", fontsize=20)
    start_button.draw(screen)
    sound_button.draw(screen)
    exit_button.draw(screen)


def draw_hud():
    for i in range(settings.HERO_MAX_HP):
        image = "heart_full" if i < hero.hp else "heart_empty"
        screen.blit(image, (settings.OFFSET_X + i * 50, 6))
    collected = level.total_coins - len(level.coins)
    screen.draw.text(f"Coins: {collected}/{level.total_coins}",
                     topright=(WIDTH - settings.OFFSET_X, 16),
                     fontsize=36, color="gold")


def draw_game_screen():
    screen.fill((0, 0, 0))
    level.draw(screen)
    for coin in coin_sprites.values():
        coin.draw()
    for enemy in enemies:
        enemy.draw()
    hero.draw()
    draw_hud()


def draw_end_screen(title, color):
    screen.fill((0, 0, 0))
    screen.draw.text(title, center=(CENTER_X, 280), fontsize=80, color=color)
    collected = level.total_coins - len(level.coins)
    screen.draw.text(f"Coins: {collected}/{level.total_coins}",
                     center=(CENTER_X, 350), fontsize=36, color="white")
    play_again_button.draw(screen)
    end_menu_button.draw(screen)


def draw_win_screen():
    draw_end_screen("YOU ESCAPED!", "gold")


def draw_lose_screen():
    draw_end_screen("GAME OVER", "red")


SCREENS = {
    "start_screen": draw_start_screen,
    "game_screen": draw_game_screen,
    "pause_screen": draw_pause_screen,
    "win_screen": draw_win_screen,
    "lose_screen": draw_lose_screen,
}


def draw():
    SCREENS[active_screen]()


def check_pickups():
    hero_cell = (hero.col, hero.row)
    if hero_cell in level.coins:
        level.coins.discard(hero_cell)
        del coin_sprites[hero_cell]
        play_sound("coin")
    if hero_cell in level.potions:
        level.potions.discard(hero_cell)
        hero.heal()
        play_sound("heal")


def check_enemy_hits():
    for enemy in enemies:
        if hero.hitbox.colliderect(enemy.hitbox) and hero.take_damage():
            play_sound("hit")


def check_game_over():
    global active_screen
    if hero.hp <= 0:
        play_sound("lose")
        active_screen = "lose_screen"
    elif (hero.col, hero.row) == level.exit and not level.coins:
        play_sound("win")
        active_screen = "win_screen"


def update(dt):
    if active_screen != "game_screen":
        return
    hero.update(dt, level)
    for enemy in enemies:
        enemy.update(dt, level)
    for coin in coin_sprites.values():
        coin.update(dt)
    check_pickups()
    check_enemy_hits()
    check_game_over()


def on_mouse_down(pos):
    global active_screen

    if active_screen == "start_screen":
        if start_button.is_clicked(pos):
            play_sound("click")
            reset_game()
            active_screen = "game_screen"
        elif sound_button.is_clicked(pos):
            toggle_sound()
        elif exit_button.is_clicked(pos):
            exit()

    elif active_screen == "pause_screen":
        if back_to_game_button.is_clicked(pos):
            play_sound("click")
            active_screen = "game_screen"
        elif back_to_main_menu_button.is_clicked(pos):
            play_sound("click")
            active_screen = "start_screen"

    elif active_screen in ("win_screen", "lose_screen"):
        if play_again_button.is_clicked(pos):
            play_sound("click")
            reset_game()
            active_screen = "game_screen"
        elif end_menu_button.is_clicked(pos):
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
