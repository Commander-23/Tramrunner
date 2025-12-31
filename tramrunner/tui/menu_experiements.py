import curses

class MenuWindow:
    def __init__(self, stdscr, menu_items, height=None, width=None, 
                 start_y=0, start_x=0, title="MENU"):
        self.stdscr = stdscr
        self.menu_items = menu_items
        self.current_row = 0
        self.title = title
        
        # Calculate dimensions if not provided
        if height is None:
            height = len(menu_items) + 4
        if width is None:
            width = max(len(item) for item in menu_items) + 10
        
        self.height = height
        self.width = width
        self.start_y = start_y
        self.start_x = start_x
        
        # Create the window
        self.win = curses.newwin(height, width, start_y, start_x)
        self.win.keypad(True)
    
    def resize(self, height, width, start_y=None, start_x=None):
        """Resize and/or reposition the menu window"""
        self.height = height
        self.width = width
        if start_y is not None:
            self.start_y = start_y
        if start_x is not None:
            self.start_x = start_x
        
        # Delete old window and create new one
        del self.win
        self.win = curses.newwin(height, width, self.start_y, self.start_x)
        self.win.keypad(True)
    
    def move(self, start_y, start_x):
        """Move the window to a new position"""
        self.start_y = start_y
        self.start_x = start_x
        self.win.mvwin(start_y, start_x)
    
    def draw(self):
        """Draw the menu in the window"""
        self.win.clear()
        h, w = self.win.getmaxyx()
        
        # Draw border
        self.win.attron(curses.color_pair(1))
        
        # Top and bottom borders
        for i in range(w):
            self.win.addstr(0, i, "#")
            #if i == 0:
            #    self.win.addstr(0, i, "╔")
            #elif i == w - 1:
            #    self.win.addstr(0, i, "╗")
            #else:
            #    self.win.addstr(0, i, "═")
        
        for i in range(w):
            #self.win.addstr(h -1, i, "#")
            if i == 0:
                self.win.addstr(h - 1, i, "╚")
            #elif i == w - 1:
            #    self.win.addstr(h - 1, i, "A")
            else:
                self.win.addstr(h - 1, i, "═")
        
        # Side borders
        for i in range(1, h - 1):
            self.win.addstr(i, 0, "║")
            self.win.addstr(i, w - 1, "║")
        
        self.win.attroff(curses.color_pair(1))
        
        # Draw title
        title_text = f" {self.title} "
        title_x = max(1, w//2 - len(title_text)//2)
        self.win.addstr(0, title_x, title_text, 
                       curses.color_pair(2) | curses.A_BOLD)
        
        # Draw menu items (ensure they fit in window)
        visible_items = min(len(self.menu_items), h - 4)
        start_item = max(0, self.current_row - visible_items + 1)
        
        for idx in range(start_item, start_item + visible_items):
            if idx >= len(self.menu_items):
                break
                
            item = self.menu_items[idx]
            y = 2 + (idx - start_item)
            
            # Truncate item if too long
            max_item_len = w - 6
            display_item = item[:max_item_len] if len(item) > max_item_len else item
            x = w//2 - len(display_item)//2
            
            if idx == self.current_row:
                if x - 2 > 0:
                    self.win.addstr(y, x - 2, "▶", curses.color_pair(3))
                self.win.addstr(y, x, display_item, 
                              curses.color_pair(3) | curses.A_BOLD)
            else:
                self.win.addstr(y, x, display_item, curses.color_pair(1))
        
        self.win.refresh()
    
    def navigate_up(self):
        if self.current_row > 0:
            self.current_row -= 1
    
    def navigate_down(self):
        if self.current_row < len(self.menu_items) - 1:
            self.current_row += 1
    
    def get_selected(self):
        return self.current_row, self.menu_items[self.current_row]
    
    def getch(self):
        return self.win.getch()


class InfoWindow:
    def __init__(self, stdscr, height, width, start_y, start_x, title="INFO"):
        self.stdscr = stdscr
        self.height = height
        self.width = width
        self.start_y = start_y
        self.start_x = start_x
        self.title = title
        self.content = []
        
        self.win = curses.newwin(height, width, start_y, start_x)
    
    def resize(self, height, width, start_y=None, start_x=None):
        self.height = height
        self.width = width
        if start_y is not None:
            self.start_y = start_y
        if start_x is not None:
            self.start_x = start_x
        
        del self.win
        self.win = curses.newwin(height, width, self.start_y, self.start_x)
    
    def set_content(self, content_lines):
        self.content = content_lines
    
    def draw(self):
        self.win.clear()
        h, w = self.win.getmaxyx()
        
        # Draw border
        self.win.border()
        
        # Draw title
        title_text = f" {self.title} "
        self.win.addstr(0, w//2 - len(title_text)//2, title_text, 
                       curses.color_pair(2) | curses.A_BOLD)
        
        # Draw content
        for idx, line in enumerate(self.content):
            if idx + 1 >= h - 1:
                break
            # Truncate line if necessary
            display_line = line[:w-3] if len(line) > w-3 else line
            self.win.addstr(idx + 1, 2, display_line)
        
        self.win.refresh()


def draw_status_bar(stdscr, text):
    h, w = stdscr.getmaxyx()
    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(h - 1, 0, " " * (w - 1))
    stdscr.addstr(h - 1, 0, text[:w-1])
    stdscr.attroff(curses.color_pair(1))
    stdscr.refresh()


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    # Get terminal dimensions
    term_h, term_w = stdscr.getmaxyx()
    
    # Create menu window (left side)
    menu_items = ["New Game", "Load Game", "Settings", "Credits", "Exit"]
    menu_width = 30
    menu_height = len(menu_items) + 4
    menu = MenuWindow(stdscr, menu_items, menu_height, menu_width, 
                      start_y=1, start_x=2, title="MAIN MENU")
    
    # Create info window (right side)
    info_width = term_w - menu_width - 6
    info_height = menu_height
    info = InfoWindow(stdscr, info_height, info_width, 
                     start_y=1, start_x=menu_width + 4, title="DETAILS")
    
    # Menu descriptions
    descriptions = {
        "New Game": [
            "Start a new adventure!",
            "",
            "- Choose your character",
            "- Select difficulty level",
            "- Begin your journey"
        ],
        "Load Game": [
            "Continue your progress",
            "",
            "Load from saved games:",
            "- Slot 1: Level 15",
            "- Slot 2: Level 8",
            "- Slot 3: Empty"
        ],
        "Settings": [
            "Configure game options",
            "",
            "Adjust:",
            "- Graphics quality",
            "- Audio levels",
            "- Controls",
            "- Display mode"
        ],
        "Credits": [
            "Game Credits",
            "",
            "Developer: Your Studio",
            "Music: Composer Name",
            "Art: Artist Name",
            "",
            "Thanks for playing!"
        ],
        "Exit": [
            "Leave the game",
            "",
            "Your progress will be saved.",
            "See you next time!"
        ]
    }
    
    # Layout modes
    layout_mode = "side_by_side"  # or "stacked" or "menu_only"
    
    def update_layout(mode):
        nonlocal layout_mode
        layout_mode = mode
        term_h, term_w = stdscr.getmaxyx()
        
        if mode == "side_by_side":
            menu.resize(menu_height, menu_width, 1, 2)
            info.resize(menu_height, term_w - menu_width - 6, 1, menu_width + 4)
        elif mode == "stacked":
            menu.resize(menu_height, term_w - 4, 1, 2)
            info.resize(10, term_w - 4, menu_height + 2, 2)
        elif mode == "menu_only":
            menu.resize(menu_height, term_w - 4, 1, 2)
    
    # Initial draw
    update_layout(layout_mode)
    
    while True:
        stdscr.clear()
        
        # Draw windows
        menu.draw()
        
        if layout_mode in ["side_by_side", "stacked"]:
            _, selected_item = menu.get_selected()
            info.set_content(descriptions.get(selected_item, ["No info available"]))
            info.draw()
        
        # Draw status bar with controls
        status = f"↑/↓: Navigate | Enter: Select | r: Resize | m: Mode | q: Quit | Mode: {layout_mode}"
        draw_status_bar(stdscr, status)
        
        key = menu.getch()
        
        if key == curses.KEY_UP:
            menu.navigate_up()
        elif key == curses.KEY_DOWN:
            menu.navigate_down()
        elif key == ord('\n'):
            idx, selected = menu.get_selected()
            if selected == "Exit":
                break
            # Show selection feedback
            stdscr.addstr(0, 2, f"Selected: {selected}", 
                         curses.color_pair(3) | curses.A_BOLD)
            stdscr.refresh()
            stdscr.getch()
        elif key == ord('r'):
            # Resize demo - make menu smaller/larger
            if menu.width == 30:
                menu.resize(menu.height, 40)
            else:
                menu.resize(menu.height, 30)
        elif key == ord('m'):
            # Cycle through layout modes
            if layout_mode == "side_by_side":
                update_layout("stacked")
            elif layout_mode == "stacked":
                update_layout("menu_only")
            else:
                update_layout("side_by_side")
        elif key == ord('q'):
            break
        elif key == curses.KEY_RESIZE:
            # Handle terminal resize
            stdscr.clear()
            update_layout(layout_mode)
    stdscr.refresh()
if __name__ == "__main__":
    curses.wrapper(main)