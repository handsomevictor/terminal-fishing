import curses
import time
from fishing_game import config
from fishing_game.game import Game

def main(stdscr, test_mode=False):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(config.FRAME_TIME_MS)
    
    config.init_colors()
    game = Game(stdscr)
    
    frames = 0
    while True:
        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            game.save_high_score()
            break
            
        game.handle_input(key)
            
        game.update()
        game.draw()
        
        if test_mode:
            frames += 1
            if frames > 50:
                break