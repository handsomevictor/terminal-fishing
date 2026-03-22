import curses
import time
from fishing_game import config
from fishing_game.game import Game

def main(stdscr):
    # Setup curses
    curses.curs_set(0)          # Hide cursor
    stdscr.nodelay(1)           # Non-blocking input
    stdscr.timeout(config.FRAME_TIME_MS) # Frame rate control
    
    config.init_colors()
    
    game = Game(stdscr)
    
    while True:
        # 1. Get input
        key = stdscr.getch()
        
        # 2. Process input
        if key == ord('q') or key == ord('Q'):
            break
            
        if key != -1:
            game.handle_input(key)
            
        # 3. Update game state
        game.update()
        
        # 4. Render
        game.draw()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
