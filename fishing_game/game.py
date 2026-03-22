import curses
import random
from fishing_game import config
from fishing_game.utils import draw_str
from fishing_game.entities.water import Water
from fishing_game.entities.fish import Fish
from fishing_game.entities.rod import Rod

class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.max_y, self.max_x = stdscr.getmaxyx()
        
        self.water_start_y = int(self.max_y * config.WATER_LEVEL_RATIO)
        self.water_height = self.max_y - self.water_start_y
        
        self.water = Water(self.water_start_y, self.water_height, self.max_x)
        self.rod = Rod(5, self.water_start_y - 3)
        self.fishes = []
        
        self.state = "MENU"
        self.score = 0
        self.bite_timer = 0
        self.reel_timer = 0
        self.target_fish = None
        self.message = "Press SPACE to start"
        self.message_timer = 0

    def spawn_fish(self):
        if len(self.fishes) < config.MAX_FISH and random.random() < config.FISH_SPAWN_CHANCE:
            self.fishes.append(Fish(self.water_start_y, self.max_y, self.max_x))

    def update(self):
        self.water.update()
        
        self.spawn_fish()
        for fish in self.fishes:
            fish.move()
            
        self.fishes = [f for f in self.fishes if not f.is_out_of_bounds()]
        
        if self.state == "CASTING":
            if self.rod.update_cast():
                self.state = "WAITING"
                
        elif self.state == "WAITING":
            for fish in self.fishes:
                if not fish.bitten:
                    dist_x = abs(fish.x - self.rod.hook_x)
                    dist_y = abs(fish.y - self.rod.hook_y)
                    if dist_x <= config.BITE_DISTANCE_X and dist_y <= config.BITE_DISTANCE_Y:
                        if random.random() < config.BITE_CHANCE:
                            self.state = "BITING"
                            self.bite_timer = config.BITE_MAX_WAIT
                            self.target_fish = fish
                            fish.bitten = True
                            break
                            
        elif self.state == "BITING":
            self.bite_timer -= 1
            if self.bite_timer <= 0:
                self.state = "IDLE"
                self.rod.reset()
                self.set_message("Fish got away...", 60)
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None
                
        elif self.state == "REELING":
            self.reel_timer -= 1
            if self.reel_timer <= 0:
                self.state = "IDLE"
                self.rod.reset()
                self.set_message("Too slow! It got away.", 60)
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None

        if self.message_timer > 0:
            self.message_timer -= 1

    def handle_input(self, key):
        if key == curses.KEY_RESIZE:
            self.max_y, self.max_x = self.stdscr.getmaxyx()
            self.water_start_y = int(self.max_y * config.WATER_LEVEL_RATIO)
            self.water_height = self.max_y - self.water_start_y
            self.water.resize(self.water_start_y, self.water_height, self.max_x)
            self.rod.player_y = self.water_start_y - 3
            
        elif self.state == "MENU":
            if key == ord(' '):
                self.state = "IDLE"
                self.set_message("Press SPACE to cast", 60)
                
        elif self.state == "IDLE":
            if key == ord(' '):
                self.state = "CASTING"
                target_x = random.randint(20, max(21, self.max_x - 10))
                target_y = random.randint(self.water_start_y + 1, self.max_y - 2)
                self.rod.cast(target_x, target_y)
                
        elif self.state == "BITING":
            if key == ord(' '):
                self.state = "REELING"
                self.reel_timer = config.REEL_TIME_LIMIT
                self.set_message("REEL! Press ENTER!", 60)
                
        elif self.state == "REELING":
            if key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                self.score += self.target_fish.points
                self.set_message(f"Caught a {self.target_fish.rarity} fish! +{self.target_fish.points} pts", 100)
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None
                self.state = "IDLE"
                self.rod.reset()

    def set_message(self, msg, duration):
        self.message = msg
        self.message_timer = duration

    def draw(self):
        self.stdscr.erase()
        
        draw_str(self.stdscr, 0, 0, f"Score: {self.score}", config.COLOR_UI)
        draw_str(self.stdscr, 0, self.max_x - 18, "Press 'q' to quit", config.COLOR_UI)
        
        draw_str(self.stdscr, self.water_start_y - 1, 0, "=" * self.max_x, config.COLOR_UI)
        
        self.water.draw(self.stdscr)
        
        for fish in self.fishes:
            fish.draw(self.stdscr)
            
        self.rod.draw(self.stdscr, self.state, self.bite_timer)
        
        if self.state == "MENU":
            draw_str(self.stdscr, self.max_y // 2, self.max_x // 2 - 8, "TERMINAL FISHING", config.COLOR_WATER)
            draw_str(self.stdscr, self.max_y // 2 + 2, self.max_x // 2 - 10, self.message, config.COLOR_UI)
        elif self.message_timer > 0:
            draw_str(self.stdscr, 2, max(0, self.max_x // 2 - len(self.message) // 2), self.message, config.COLOR_ALERT)
            
        if self.state == "REELING":
            bar_len = 20
            progress = int((self.reel_timer / config.REEL_TIME_LIMIT) * bar_len)
            bar = "[" + "#" * progress + " " * (bar_len - progress) + "]"
            draw_str(self.stdscr, self.max_y // 2, self.max_x // 2 - 11, bar, config.COLOR_ALERT)

        self.stdscr.refresh()
