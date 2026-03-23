from fishing_game.utils import draw_str, calculate_parabola
from fishing_game import config

class Rod:
    def __init__(self, player_x, player_y):
        self.player_x = player_x
        self.player_y = player_y
        self.hook_x = None
        self.hook_y = None
        
        self.casting_path = []
        self.cast_frame = 0
        
    def cast(self, target_x, target_y):
        # Calculate casting arc
        self.casting_path = calculate_parabola(
            self.player_x + 5, self.player_y - 1, 
            target_x, target_y, 
            config.CASTING_FRAMES
        )
        self.cast_frame = 0
        
    def update_cast(self):
        """Update hook position during cast. Returns True if finished."""
        if self.cast_frame < len(self.casting_path):
            self.hook_x, self.hook_y = self.casting_path[self.cast_frame]
            self.cast_frame += 1
            return False
        return True
        
    def reset(self):
        self.hook_x = None
        self.hook_y = None
        self.casting_path = []
        self.cast_frame = 0
        
    def draw(self, stdscr, state, bite_timer=0):
        # Draw player and rod base
        draw_str(stdscr, self.player_y, self.player_x, "  O", config.COLOR_UI)
        draw_str(stdscr, self.player_y + 1, self.player_x, " /|\\/", config.COLOR_ROD)
        draw_str(stdscr, self.player_y + 2, self.player_x, " / \\", config.COLOR_UI)
        
        # Draw line and hook
        if self.hook_x is not None and self.hook_y is not None:
            # Draw fishing line (from player rod tip down to hook)
            rod_tip_x = self.player_x + 5
            rod_tip_y = self.player_y - 1
            
            if state in ["WAITING", "BITING"]:
                # Draw vertical line from rod tip level down to hook
                for ly in range(rod_tip_y, self.hook_y):
                    draw_str(stdscr, ly, self.hook_x, "|", config.COLOR_HOOK)

            if state == "CASTING":
                draw_str(stdscr, self.hook_y, self.hook_x, " J ", config.COLOR_HOOK)
            elif state in ["WAITING", "BITING", "REELING"]:
                # Draw larger bobber
                symbol = "(O)"
                if state == "BITING":
                    symbol = "[!]" if bite_timer % 2 == 0 else "(O)"
                    draw_str(stdscr, self.hook_y - 1, self.hook_x, " !! ", config.COLOR_ALERT)
                draw_str(stdscr, self.hook_y, self.hook_x - 1, symbol, config.COLOR_HOOK)
