import settings

MAP = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WH...W......W.....CW",
    "W....W..C...W......W",
    "W.C..W......W..g...W",
    "W....WWW.WWWW......W",
    "W..................W",
    "WWWW.WWWWWW.WWWW.WWW",
    "W.........W.....W..W",
    "W..s...C..W..C..W.PW",
    "W.........W.....W..W",
    "WWWWW.WWWWW..s..W.WW",
    "W.C.........WWWWW..W",
    "W....g.........C...W",
    "W.....C........W..EW",
    "WWWWWWWWWWWWWWWWWWWW",
]


class Level:
    def __init__(self, layout):
        self.layout = layout
        self.walls = set()
        self.enemy_spawns = []
        for row, line in enumerate(layout):
            for col, char in enumerate(line):
                if char == "W":
                    self.walls.add((col, row))
                elif char == "H":
                    self.hero_start = (col, row)
                elif char in "gs":
                    self.enemy_spawns.append((col, row))
       

    def is_wall(self, col, row):
        return (col, row) in self.walls
    
    def draw(self, screen):
        for row, line in enumerate(self.layout):
            for col, char in enumerate(line):
                pos = cell_to_pixel(col, row)
                if char == "W":
                    screen.blit("wall", pos)
                else:
                    screen.blit("floor_1", pos)

                
def cell_to_pixel(col, row):
    x = settings.OFFSET_X + col * settings.TILE_SIZE
    y = settings.OFFSET_Y + row * settings.TILE_SIZE
    return x, y

def cell_to_foot(col, row):
    x = settings.OFFSET_X + col * settings.TILE_SIZE
    y = settings.OFFSET_Y + row * settings.TILE_SIZE
    
    bottom_center = (x + settings.TILE_SIZE // 2, y + settings.TILE_SIZE)
    return bottom_center