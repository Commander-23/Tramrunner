import curses
import time
import stop_info_tui

class dvb_curse:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) # Hide Curser
        self.setup_colors()
        self.create_windows()

    def setup_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    def create_windows(self):
        max_y, max_x = self.stdscr.getmaxyx()

        self.header = curses.newwin(3, max_x, 0, 0)
        
        # Left panel - for menu/navigation
        left_width = max_x // 3
        self.left_panel = curses.newwin(max_y - 6 , left_width        , 3, 0)
        # Right panel - for content display
        self.right_panel = curses.newwin(max_y - 6, max_x - left_width, 3, left_width)
        # Status bar at bottom
        self.status = curses.newwin(3, max_x, max_y - 3, 0)

    def draw_header(self, title):
        self.header.clear()
        self.header.box()

        # Center the title
        max_y, max_x = self.header.getmaxyx()
        x = (max_x - len(title)) // 2
        self.header.addstr(1, x, title, curses.color_pair(1) | curses.A_BOLD)
        self.header.refresh()
    
    def draw_left_panel(self, items, selected):
        self.left_panel.clear()
        self.left_panel.box()
        self.left_panel.addstr(0, 2, " Menu ", curses.A_BOLD)
        
        for idx, item in enumerate(items):
            y = idx + 2
            if idx == selected:
                self.left_panel.addstr(y, 2, f"> {item}", curses.A_REVERSE)
            else:
                self.left_panel.addstr(y, 2, f"  {item}")
        
        self.left_panel.refresh()
        
    def draw_right_panel(self, content_lines):
        self.right_panel.clear()
        self.right_panel.box()
        self.right_panel.addstr(0, 2, " Output ", curses.A_BOLD)
        
        max_y, max_x = self.right_panel.getmaxyx()
        
        for idx, line in enumerate(content_lines):
            if idx + 1 >= max_y - 1:  # Leave room for border
                break
            safe_line = line[:max_x - 3]  # Truncate if needed
            self.right_panel.addstr(idx + 1, 1, safe_line)
        
        self.right_panel.refresh()
        
    def draw_status(self, message):
        self.status.clear()
        self.status.box()
        self.status.addstr(1, 2, message, curses.color_pair(2))
        self.status.refresh()

    def run(self):
        menu_items = ["Test_complicated", "Test_simple", "Show Stats", "Quit"]
        selected = 0
        content = ["Welcome! Select an option from the menu."]
        
        self.draw_header("My Multi-Window Application")
        self.draw_status("Press ↑/↓ to navigate, Enter to select, Q to quit")
        
        self.stdscr.nodelay(False)
        
        while True:
            self.draw_left_panel(menu_items, selected)
            self.draw_right_panel(content)
            
            key = self.stdscr.getch()
            
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(menu_items) - 1:
                selected += 1
            elif key == ord('\n'):
                if selected == 3:  # Quit
                    break
                else:
                    content = self.handle_selection(selected)
            elif key == ord('q') or key == ord('Q'):
                break
                
    def handle_selection(self, selection):

        """Simulate processing based on menu selection"""
        if selection == 0:

            return [f"{i}" for i in stop_info_tui.stop_info_tui("rac")]
        elif selection == 1:
            return ["Processing...", "Step 1 complete", "Step 2 complete"]
        elif selection == 2:
            return ["Statistics:", "Items: 42", "Average: 3.14"]
        return []

def main(stdscr):
    app = dvb_curse(stdscr)
    app.run()
    app.re

if __name__ == "__main__":
    stop_info_tui.stop_info_tui("rac")
    curses.wrapper(main)