import random

from pgzero.actor import Actor
from pgzero.builtins import keyboard
from pgzero.rect import Rect

import settings
from level import cell_to_foot

DIRECTIONS = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}


def make_animations(name, states=("idle", "run", "idle_left", "run_left"),
                    frame_count=4):
    return {
        state: [f"{name}_{state}_{i}" for i in range(frame_count)]
        for state in states
    }


class AnimatedSprite:
    frame_time = 0.12

    def __init__(self, animations, pos):
        self.animations = animations
        self.state = "idle"
        self.frame = 0
        self.timer = 0.0
        self.actor = Actor(animations["idle"][0], pos,
                           anchor=("center", "bottom"))

    def set_state(self, state):
        if state == self.state:
            return
        self.state = state
        self.frame = 0
        self.timer = 0.0
        self.actor.image = self.animations[state][0]

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer -= self.frame_time
            frames = self.animations[self.state]
            self.frame = (self.frame + 1) % len(frames)
            self.actor.image = frames[self.frame]

    def draw(self):
        self.actor.draw()


class GridMover(AnimatedSprite):
    def __init__(self, animations, col, row, step_time):
        super().__init__(animations, cell_to_foot(col, row))
        self.col = col
        self.row = row
        self.step_time = step_time
        self.start = self.actor.pos
        self.target = self.actor.pos
        self.elapsed = step_time
        self.facing = "right"

    @property
    def is_moving(self):
        return self.elapsed < self.step_time

    @property
    def hitbox(self):
        box = Rect(0, 0, 28, 28)
        box.center = (self.actor.x, self.actor.y - settings.TILE_SIZE // 2)
        return box

    def move_to(self, col, row):
        if col < self.col:
            self.facing = "left"
        elif col > self.col:
            self.facing = "right"
        self.col = col
        self.row = row
        self.start = self.actor.pos
        self.target = cell_to_foot(col, row)
        self.elapsed = 0.0

    def update_motion(self, dt):
        if not self.is_moving:
            return
        self.elapsed = min(self.elapsed + dt, self.step_time)
        t = self.elapsed / self.step_time
        x = self.start[0] + (self.target[0] - self.start[0]) * t
        y = self.start[1] + (self.target[1] - self.start[1]) * t
        self.actor.pos = (x, y)

    def animation_state(self):
        state = "run" if self.is_moving else "idle"
        if self.facing == "left":
            state += "_left"
        return state


class Hero(GridMover):
    def __init__(self, col, row):
        super().__init__(make_animations("hero"), col, row,
                         settings.HERO_STEP_TIME)
        self.hp = settings.HERO_START_HP
        self.invulnerable_timer = 0.0

    def take_damage(self):
        if self.invulnerable_timer > 0:
            return False
        self.hp -= 1
        self.invulnerable_timer = settings.INVULNERABLE_TIME
        return True

    def heal(self):
        self.hp = min(self.hp + 1, settings.HERO_MAX_HP)

    def handle_input(self, level):
        if self.is_moving:
            return

        direction = None
        if keyboard.left or keyboard.a:
            direction = "left"
        elif keyboard.right or keyboard.d:
            direction = "right"
        elif keyboard.up or keyboard.w:
            direction = "up"
        elif keyboard.down or keyboard.s:
            direction = "down"

        if direction is not None:
            dx, dy = DIRECTIONS[direction]
            new_col = self.col + dx
            new_row = self.row + dy
            if not level.is_wall(new_col, new_row):
                self.move_to(new_col, new_row)

    def update(self, dt, level):
        self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)
        self.update_motion(dt)
        self.handle_input(level)
        self.set_state(self.animation_state())
        super().update(dt)

    def draw(self):
        blinking = int(self.invulnerable_timer * 10) % 2 == 1
        if self.invulnerable_timer > 0 and blinking:
            return
        super().draw()


class Enemy(GridMover):
    name = ""
    step_time = 0.3
    wait_time = 0.5

    def __init__(self, col, row):
        super().__init__(make_animations(self.name), col, row,
                         self.step_time)
        self.wait_timer = 0.0
        self.territory = self.make_territory(col, row)

    def make_territory(self, col, row):
        raise NotImplementedError

    def can_enter(self, col, row, level):
        return (self.territory.collidepoint(col, row)
                and not level.is_wall(col, row))

    def choose_step(self, level):
        raise NotImplementedError

    def update(self, dt, level):
        self.update_motion(dt)
        if not self.is_moving:
            self.wait_timer += dt
            if self.wait_timer >= self.wait_time:
                self.wait_timer = 0.0
                step = self.choose_step(level)
                if step is not None:
                    self.move_to(self.col + step[0], self.row + step[1])
        self.set_state(self.animation_state())
        super().update(dt)


class Goblin(Enemy):
    name = "goblin"
    step_time = 0.25
    wait_time = 0.4

    def make_territory(self, col, row):
        return Rect(col - 2, row - 2, 5, 5)

    def choose_step(self, level):
        options = []
        for direction in DIRECTIONS.values():
            new_col = self.col + direction[0]
            new_row = self.row + direction[1]
            if self.can_enter(new_col, new_row, level):
                options.append(direction)
        if options:
            return random.choice(options)
        return None


class Skeleton(Enemy):
    name = "skeleton"
    step_time = 0.4
    wait_time = 0.7

    def __init__(self, col, row):
        super().__init__(col, row)
        self.direction = (1, 0)

    def make_territory(self, col, row):
        return Rect(col - 3, row, 7, 1)

    def choose_step(self, level):
        new_col = self.col + self.direction[0]
        new_row = self.row + self.direction[1]
        if self.can_enter(new_col, new_row, level):
            return self.direction

        self.direction = (-self.direction[0], -self.direction[1])
        new_col = self.col + self.direction[0]
        new_row = self.row + self.direction[1]
        if self.can_enter(new_col, new_row, level):
            return self.direction
        return None
