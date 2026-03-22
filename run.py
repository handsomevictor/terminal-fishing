import sys
import os
import curses
import argparse

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from fishing_game.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run in test mode (auto-exit)")
    args = parser.parse_args()

    try:
        curses.wrapper(main, test_mode=args.test)
    except KeyboardInterrupt:
        pass