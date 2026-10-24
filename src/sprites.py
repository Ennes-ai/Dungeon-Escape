from pgzero.actor import Actor


def make_animations(name, states=("idle", "run"), frame_count=4):
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