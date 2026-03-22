import curses
import random

def draw_str(stdscr, y, x, string, color_pair=0):
    """Safely draw a string to the screen avoiding curses bounds errors."""
    try:
        max_y, max_x = stdscr.getmaxyx()
        y = int(y)
        x = int(x)
        if 0 <= y < max_y and 0 <= x < max_x:
            # truncate string if it exceeds right bound
            visible_length = min(len(string), max_x - x - 1)
            if visible_length > 0:
                stdscr.addstr(y, x, string[:visible_length], curses.color_pair(color_pair))
    except curses.error:
        pass # Ignore drawing outside bounds

def calculate_parabola(start_x, start_y, end_x, end_y, frames):
    """Calculate trajectory points for casting animation."""
    points = []
    if frames <= 1:
        return [(end_x, end_y)]
        
    for i in range(frames):
        t = i / (frames - 1)
        
        peak_y = min(start_y, end_y) - max(5, abs(start_x - end_x) // 4)
        
        # Bezier curve for simplicity
        cx = (start_x + end_x) / 2
        cy = peak_y
        
        bx = int((1-t)**2 * start_x + 2*(1-t)*t * cx + t**2 * end_x)
        by = int((1-t)**2 * start_y + 2*(1-t)*t * cy + t**2 * end_y)
        
        points.append((bx, by))
        
    return points
