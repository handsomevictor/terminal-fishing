import curses

# --- Game Display ---
FPS = 20
FRAME_TIME_MS = int(1000 / FPS)

# --- Colors ---
# Color pair IDs
COLOR_WATER = 1
COLOR_FISH_NORMAL = 2
COLOR_FISH_RARE = 3
COLOR_FISH_EPIC = 4
COLOR_ROD = 5
COLOR_HOOK = 6
COLOR_UI = 7
COLOR_ALERT = 8

def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(COLOR_WATER, curses.COLOR_CYAN, -1)
    curses.init_pair(COLOR_FISH_NORMAL, curses.COLOR_WHITE, -1)
    curses.init_pair(COLOR_FISH_RARE, curses.COLOR_BLUE, -1)
    curses.init_pair(COLOR_FISH_EPIC, curses.COLOR_MAGENTA, -1)
    curses.init_pair(COLOR_ROD, curses.COLOR_YELLOW, -1)
    curses.init_pair(COLOR_HOOK, curses.COLOR_WHITE, -1)
    curses.init_pair(COLOR_UI, curses.COLOR_GREEN, -1)
    curses.init_pair(COLOR_ALERT, curses.COLOR_RED, -1)

# --- Physics & Gameplay ---
WATER_LEVEL_RATIO = 0.3  # Water surface is at 30% of screen height from top
BITE_DISTANCE_X = 5      # X distance threshold for biting
BITE_DISTANCE_Y = 2      # Y distance threshold for biting

# State timings
CASTING_FRAMES = 10      # How many frames the casting animation takes
BITE_MAX_WAIT = 30       # Frames before fish loses interest if not bitten
REEL_TIME_LIMIT = 20     # Frames to react for QTE (1 second at 20fps)

# Probabilities
FISH_SPAWN_CHANCE = 0.05 # Chance per frame to spawn a new fish if under max
MAX_FISH = 5
BITE_CHANCE = 0.05       # Base chance per frame for fish near hook to bite

# --- Fish Types ---
# (symbol, speed, points, rarity, color_pair)
FISH_TYPES = [
    ("><>", 1.0, 10, "Common", COLOR_FISH_NORMAL),
    (">=<", 1.5, 20, "Uncommon", COLOR_FISH_NORMAL),
    ("<°)))><", 2.0, 50, "Rare", COLOR_FISH_RARE),
    ("~o=<>", 3.0, 100, "Epic", COLOR_FISH_EPIC),
]
