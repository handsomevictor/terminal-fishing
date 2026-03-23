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
        self.state = "WANDERING" # WANDERING, CURIOUS, FLEEING
        self.target_hook = None
        
    def move(self, hook_pos=None):
        if self.bitten:
            # Add subtle struggling movement when bitten
            if random.random() < 0.3:
                self.x += random.choice([-0.5, 0.5])
                self.y += random.choice([-0.5, 0.5])
                self.y = max(self.water_start_y + 1, min(self.y, self.max_y - 2))
            return

        # AI Behavior when hook is present
        if hook_pos and self.state == "WANDERING":
            hx, hy = hook_pos
            dist = abs(self.x - hx) + abs(self.y - hy)
            if dist < 20: # Can sense the hook
                if self.rarity == "Trash":
                    pass # Trash doesn't care
                elif random.random() < 0.3: # 30% chance to get scared and flee
                    self.state = "FLEEING"
                    self.direction = -1 if self.x < hx else 1
                    self.speed *= 2
                elif random.random() < 0.5: # 50% chance to get curious
                    self.state = "CURIOUS"
                    self.target_hook = hook_pos

        if self.state == "CURIOUS" and hook_pos:
            hx, hy = hook_pos
            # Move towards hook
            if self.x < hx - 2:
                self.direction = 1
                self.x += self.speed * 0.8
            elif self.x > hx + 2:
                self.direction = -1
                self.x -= self.speed * 0.8
            
            if self.y < hy:
                self.y += self.speed * 0.5
            elif self.y > hy:
                self.y -= self.speed * 0.5
                
            # If hook disappears, go back to wandering
            if random.random() < 0.05:
                self.state = "WANDERING"
                
        else:
            # WANDERING or FLEEING
            self.x += self.speed * self.direction
            
            # Random vertical movement
            if random.random() < 0.1:
                self.y += random.choice([-1, 1])
                
        # Constrain Y to water bounds
        self.y = max(self.water_start_y + 1, min(self.y, self.max_y - 2))
            
    def is_out_of_bounds(self):
        if self.direction == 1 and self.x > self.max_x:
            return True
        elif self.direction == -1 and self.x < -len(self.symbol):
            return True
        return False
        
    def draw(self, stdscr):
        draw_str(stdscr, int(self.y), int(self.x), self.symbol, self.color)
