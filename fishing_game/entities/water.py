import random
from fishing_game.utils import draw_str
from fishing_game import config

class Water:
    def __init__(self, start_y, height, width):
        self.start_y = start_y
        self.height = height
        self.width = width
        self.chars = ['~', '-', '≈']
        # Initialize water surface
        self.surface = [[random.choice(self.chars) for _ in range(width)] for _ in range(height)]
        
    def update(self):
        """Randomly animate water ripples"""
        for _ in range(max(1, self.width * self.height // 20)):
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            self.surface[y][x] = random.choice(self.chars)
            
    def draw(self, stdscr):
        for y in range(self.height):
            row_str = "".join(self.surface[y])
            draw_str(stdscr, self.start_y + y, 0, row_str, config.COLOR_WATER)

    def resize(self, start_y, height, width):
        self.start_y = start_y
        self.height = height
        self.width = width
        self.surface = [[random.choice(self.chars) for _ in range(width)] for _ in range(height)]
