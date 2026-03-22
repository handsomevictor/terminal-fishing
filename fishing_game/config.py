import curses

FPS = 20
FRAME_TIME_MS = int(1000 / FPS)

COLOR_WATER = 1
COLOR_FISH_NORMAL = 2
COLOR_FISH_RARE = 3
COLOR_FISH_EPIC = 4
COLOR_ROD = 5
COLOR_HOOK = 6
COLOR_UI = 7
COLOR_ALERT = 8
COLOR_TRASH = 9

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
    curses.init_pair(COLOR_TRASH, curses.COLOR_BLACK, -1)

WATER_LEVEL_RATIO = 0.3
BITE_DISTANCE_X = 5
BITE_DISTANCE_Y = 2

CASTING_FRAMES = 10
BITE_MAX_WAIT = 30
REEL_TIME_LIMIT = 20

FISH_SPAWN_CHANCE = 0.05
MAX_FISH = 6
BITE_CHANCE = 0.05

FISH_TYPES = [
    ("><>", 1.0, 10, "Common", COLOR_FISH_NORMAL),
    (">=<", 1.5, 20, "Uncommon", COLOR_FISH_NORMAL),
    ("<°)))><", 2.0, 50, "Rare", COLOR_FISH_RARE),
    ("~o=<>", 3.0, 100, "Epic", COLOR_FISH_EPIC),
    ("BOOT", 0.5, -10, "Trash", COLOR_TRASH),
    ("CAN", 0.8, -5, "Trash", COLOR_TRASH),
]