import curses
import random
import json
import os
from fishing_game import config
from fishing_game.utils import draw_str
from fishing_game.entities.water import Water
from fishing_game.entities.fish import Fish
from fishing_game.entities.rod import Rod

SAVE_FILE = "save.json"

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
        self.high_score = self.load_high_score()
        self.combo = 0
        self.bite_timer = 0
        self.reel_timer = 0
        self.target_fish = None
        self.message = "Press SPACE to start"
        self.message_timer = 0
        
        # Casting mechanics
        self.charging = False
        self.charge_power = 0.0  # 0.0 to 1.0
        self.charge_direction = 1  # 1 for increasing, -1 for decreasing

    def load_high_score(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("high_score", 0)
            except:
                return 0
        return 0

    def save_high_score(self):
        if self.score > self.high_score:
            with open(SAVE_FILE, "w") as f:
                json.dump({"high_score": self.score}, f)

    def spawn_fish(self):
        spawn_chance = config.FISH_SPAWN_CHANCE + (self.score * 0.0001) # Dynamic difficulty
        if len(self.fishes) < config.MAX_FISH and random.random() < spawn_chance:
            self.fishes.append(Fish(self.water_start_y, self.max_y, self.max_x))

    def update(self):
        if self.max_y < 15 or self.max_x < 40:
            return # Pause update if screen too small

        self.water.update()
        self.spawn_fish()
        
        # Handle charging logic (Ping-pong power meter)
        if self.state == "IDLE" and self.charging:
            self.charge_power += 0.05 * self.charge_direction
            if self.charge_power >= 1.0:
                self.charge_power = 1.0
                self.charge_direction = -1
            elif self.charge_power <= 0.1:
                self.charge_power = 0.1
                self.charge_direction = 1

        for fish in self.fishes:
            # Pass hook coordinates to fish for AI reactions
            hook_pos = (self.rod.hook_x, self.rod.hook_y) if self.state in ["WAITING", "BITING"] else None
            fish.move(hook_pos)
            
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
                            # Shorter bite window at higher scores
                            self.bite_timer = max(10, config.BITE_MAX_WAIT - (self.score // 50))
                            self.target_fish = fish
                            fish.bitten = True
                            break
                            
        elif self.state == "BITING":
            self.bite_timer -= 1
            if self.bite_timer <= 0:
                self.state = "IDLE"
                self.rod.reset()
                self.combo = 0
                self.set_message("Fish got away... You missed the bite.", 60)
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None
                
        elif self.state == "REELING":
            self.reel_timer -= 1
            if self.reel_timer <= 0:
                self.state = "IDLE"
                self.rod.reset()
                self.combo = 0
                self.set_message("Too slow! It got away.", 60)
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None

        if self.message_timer > 0:
            self.message_timer -= 1

    def handle_input(self, key):
        if key == curses.KEY_RESIZE:
            self.max_y, self.max_x = self.stdscr.getmaxyx()
            if self.max_y >= 15 and self.max_x >= 40:
                self.water_start_y = int(self.max_y * config.WATER_LEVEL_RATIO)
                self.water_height = self.max_y - self.water_start_y
                self.water.resize(self.water_start_y, self.water_height, self.max_x)
                self.rod.player_y = self.water_start_y - 3
            
        elif self.state == "MENU":
            if key == ord(' '):
                self.state = "IDLE"
                self.set_message("Hold SPACE to charge, release to cast!", 100)
                
        elif self.state == "IDLE":
            if key == ord(' '):
                # Start charging
                if not self.charging:
                    self.charging = True
                    self.charge_power = 0.1
                    self.charge_direction = 1
            elif self.charging and key == -1:
                # Key released (non-blocking input returns -1 when nothing is pressed)
                # We need a way to detect release. Since curses doesn't have explicit KeyUp events easily,
                # we'll simulate it: if we were charging and now we see NO key (or specifically not space),
                # we cast!
                self.charging = False
                self.state = "CASTING"
                
                # Calculate target based on power
                min_distance = 15
                max_distance = self.max_x - self.rod.player_x - 10
                distance = int(min_distance + (max_distance - min_distance) * self.charge_power)
                target_x = self.rod.player_x + distance
                target_y = random.randint(self.water_start_y + 1, self.max_y - 2)
                
                self.rod.cast(target_x, target_y)
                
        elif self.state == "WAITING":
            if key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                # Active reeling: check if any fish is near the hook
                caught = False
                for fish in self.fishes:
                    dist_x = abs(fish.x - self.rod.hook_x)
                    dist_y = abs(fish.y - self.rod.hook_y)
                    # Slightly larger catch radius than bite radius
                    if dist_x <= config.BITE_DISTANCE_X + 2 and dist_y <= config.BITE_DISTANCE_Y + 1:
                        # Success chance based on distance
                        chance = 1.0 - (dist_x + dist_y * 2) * 0.1
                        if random.random() < chance:
                            self.target_fish = fish
                            caught = True
                            break
                
                if caught:
                    multiplier = 1 + (self.combo * 0.1)
                    earned = int(self.target_fish.points * multiplier)
                    self.score += earned
                    if earned > 0:
                        self.combo += 1
                        self.set_message(f"Active Catch: {self.target_fish.rarity}! +{earned} (Combo x{self.combo})", 100)
                    else:
                        self.combo = 0
                        self.set_message(f"Eww, snagged a {self.target_fish.rarity}. {earned} pts", 100)
                    
                    if self.target_fish in self.fishes:
                        self.fishes.remove(self.target_fish)
                else:
                    self.combo = 0
                    self.set_message("Pulled up nothing but water...", 60)
                
                self.target_fish = None
                self.state = "IDLE"
                self.rod.reset()
                
        elif self.state == "BITING":
            if key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                # If they press enter exactly during the bite flash, they auto-catch it!
                multiplier = 1 + (self.combo * 0.1)
                earned = int(self.target_fish.points * multiplier)
                self.score += earned
                if earned > 0:
                    self.combo += 1
                    self.set_message(f"Perfect Catch: {self.target_fish.rarity}! +{earned} (Combo x{self.combo})", 100)
                else:
                    self.combo = 0
                    self.set_message(f"Eww, snagged a {self.target_fish.rarity}. {earned} pts", 100)
                
                if self.target_fish in self.fishes:
                    self.fishes.remove(self.target_fish)
                self.target_fish = None
                self.state = "IDLE"
                self.rod.reset()
                
        elif self.state == "REELING":
            if key in [ord('\n'), curses.KEY_ENTER, 10, 13]:
                multiplier = 1 + (self.combo * 0.1)
                earned = int(self.target_fish.points * multiplier)
                self.score += earned
                if earned > 0:
                    self.combo += 1
                    self.set_message(f"Caught {self.target_fish.rarity}! +{earned} (Combo x{self.combo})", 100)
                else:
                    self.combo = 0
                    self.set_message(f"Eww, a {self.target_fish.rarity}. {earned} pts", 100)
                
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
        
        if self.max_y < 15 or self.max_x < 40:
            draw_str(self.stdscr, 0, 0, "Terminal too small! Please resize.", config.COLOR_ALERT)
            self.stdscr.refresh()
            return

        draw_str(self.stdscr, 0, 0, f"Score: {self.score} | High Score: {self.high_score} | Combo: {self.combo}", config.COLOR_UI)
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
            
        if self.state == "IDLE" and self.charging:
            bar_len = 20
            progress = int(self.charge_power * bar_len)
            bar = "[" + "=" * progress + " " * (bar_len - progress) + "]"
            color = config.COLOR_ALERT if self.charge_power > 0.8 else config.COLOR_UI
            draw_str(self.stdscr, self.max_y // 2, self.max_x // 2 - 11, "POWER: " + bar, color)
            
        if self.state == "REELING":
            bar_len = 20
            progress = int((self.reel_timer / config.REEL_TIME_LIMIT) * bar_len)
            bar = "[" + "#" * progress + " " * (bar_len - progress) + "]"
            draw_str(self.stdscr, self.max_y // 2, self.max_x // 2 - 11, bar, config.COLOR_ALERT)

        # Bite Flash effect
        if self.state == "BITING" and self.bite_timer % 4 < 2:
            draw_str(self.stdscr, 0, self.max_x // 2 - 4, " BITE! ", config.COLOR_ALERT, curses.A_REVERSE)

        self.stdscr.refresh()