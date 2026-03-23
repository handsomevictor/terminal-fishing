import curses
import random
from typing import List, Tuple, Any

def draw_str(stdscr: Any, y: int, x: int, string: str, color_pair: int = 0, attr: int = 0) -> None:
    """Safely draw a string to the screen avoiding curses bounds errors."""
    try:
        max_y, max_x = stdscr.getmaxyx()
        y = int(y)
        x = int(x)
        if 0 <= y < max_y and 0 <= x < max_x:
            visible_length = min(len(string), max_x - x - 1)
            if visible_length > 0:
                try:
                    stdscr.addstr(y, x, string[:visible_length], curses.color_pair(color_pair) | attr)
                except curses.error:
                    pass # curses sometimes throws even when bounds seem correct (e.g. bottom-right corner)
    except Exception:
        pass 

def calculate_parabola(start_x: int, start_y: int, end_x: int, end_y: int, frames: int) -> List[Tuple[int, int]]:
    """Calculate trajectory points for casting animation."""
    points = []
    if frames <= 1:
        return [(end_x, end_y)]
        
    for i in range(frames):
        t = i / (frames - 1)
        peak_y = min(start_y, end_y) - max(5, abs(start_x - end_x) // 4)
        
        cx = (start_x + end_x) / 2
        cy = peak_y
        
        bx = int((1-t)**2 * start_x + 2*(1-t)*t * cx + t**2 * end_x)
        by = int((1-t)**2 * start_y + 2*(1-t)*t * cy + t**2 * end_y)
        
        points.append((bx, by))
        
    return points