import sys
import os
import curses

# Add current directory to python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fishing_game.main import main

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
