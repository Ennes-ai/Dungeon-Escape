from pgzero.actor import Actor
from level import cell_to_foot
from pgzero.builtins import keyboard
import settings


def make_animations(name, states=("idle", "run", "idle_left", "run_left"),
                    frame_count=4):
    return {
        state: [f"{name}_{state}_{i}" for i in range(frame_count)]
        for state in states
    }

DIRECTIONS = {
    "left": (-1, 0),
    "right": (1, 0),
    "up": (0, -1),
    "down": (0, 1),
}

class AnimatedSprite:
    frame_time = 0.12
    
    def __init__(self, animations, pos):
        self.animations = animations
        self.state = "idle"
        self.frame = 0
        self.timer = 0.0
        self.actor = Actor(animations["idle"][0], pos, anchor=("center", "bottom"))
        
    
    def set_state(self, state):
        if state == self.state:
            return
        else:
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
    def __init__(self,animations, col, row, step_time):
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
        super().__init__(make_animations("hero"), col, row, settings.HERO_STEP_TIME)

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
        self.update_motion(dt)
        self.handle_input(level)
        self.set_state(self.animation_state())
        super().update(dt)