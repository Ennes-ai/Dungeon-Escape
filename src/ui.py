from pgzero.rect import Rect


class Button:
    def __init__(self, text, center, color="white", width=240, height=56,
                 fontsize=25):
        self.text = text
        self.color = color
        self.fontsize = fontsize
        self.rect = Rect(0, 0, width, height)
        self.rect.center = center

    def draw(self, screen):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.rect(self.rect, "white")
        screen.draw.text(self.text, center=self.rect.center, color="white",
                         fontsize=self.fontsize)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
