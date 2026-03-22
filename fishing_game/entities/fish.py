import random
from fishing_game.utils import draw_str
from fishing_game import config

class Fish:
    def __init__(self, water_start_y, max_y, max_x):
        symbol, speed, points, rarity, color = random.choice(config.FISH_TYPES)
        self.symbol = symbol
        self.speed = speed
        self.points = points
        self.rarity = rarity
        self.color = color
        
        self.direction = random.choice([-1, 1])
        if self.direction == 1:
            self.x = 0
            self.symbol = self.symbol  # Right facing
        else:
            self.x = max_x - len(self.symbol)
            # Reverse string for left facing
            self.symbol = self.symbol[::-1]
            self.symbol = self.symbol.replace('<', 'TEMP').replace('>', '<').replace('TEMP', '>')
            
        # Spawn somewhere below water surface
        self.y = random.randint(water_start_y + 1, max_y - 2)
        
        self.water_start_y = water_start_y
        self.max_y = max_y
        self.max_x = max_x
        self.bitten = False
        
    def move(self):
        if not self.bitten:
            self.x += self.speed * self.direction
            
            # Random vertical movement
            if random.random() < 0.1:
                self.y += random.choice([-1, 1])
                self.y = max(self.water_start_y + 1, min(self.y, self.max_y - 2))
            
    def is_out_of_bounds(self):
        if self.direction == 1 and self.x > self.max_x:
            return True
        elif self.direction == -1 and self.x < -len(self.symbol):
            return True
        return False
        
    def draw(self, stdscr):
        draw_str(stdscr, int(self.y), int(self.x), self.symbol, self.color)
