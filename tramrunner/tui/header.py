import curses

class MenuWindow:
    def __init__(self, stdscr, menu_items, height, width, y ,x):
        self.stdscr = stdscr
        self.menu_items = menu_items

        if height is None:
            height = len(self.menu_items) + 4
        if width is None:
            width = max(len(item) for item in menu_items) + 4
        if width == 0:
            screen_h, screen_w = stdscr.getmaxyx()
            width = screen_w

        self.win = curses.newwin(height, width, y, x)
        self.title = "Title"
    
    def move(self, start_y, start_x):
        self.start_y = start_y
        self.start_x = start_x
        self.win.mvwin(start_y, start_x)
    
    def render_w_border(self):
        self.win.clear()
        win_h, win_w = self.win.getmaxyx()

        self.win.addstr(2, 2, str(self.menu_items[1]))

        # Top border
        for i in range(win_w):
            if i == 0:
                self.win.insstr(0, i, "╔")
            elif i == win_w - 1:
                self.win.insstr(0, i, "╗")
            else:
                self.win.insstr(0, i, "═")
        # Bottom border
        for i in range(win_w):
            if i == 0:
                self.win.insstr(win_h -1, i, "╚")
            elif i == win_w - 1:
                self.win.insstr(win_h -1, i, "╝")
            else:
                self.win.insstr(win_h -1, i, "═" )
        # Side border
        for i in range(1, win_h -1):
            self.win.insstr(i, 0, "║")
            self.win.insstr(i, win_w - 1, "║")
        
        # Draw Title
        title_text = f" {self.title} "
        title_x = max(1, win_w//2 - len(title_text)//2)
        self.win.addstr(0, title_x, title_text, curses.A_BOLD)

        self.win.refresh()


class Header:
    def __init__(self, stdscr, title, menu_items):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()

        self.title_win = curses.newwin(1, max_w, 0,0) # One Line Tall, Across whole Terminal, Top-left of page
        self.p_bar_win = curses.newwin(1, max_w, 1,0) # One Line Tall, Across whole Terminal, Below the Title Bar, with Text elements Conncting
        
        self.title = title
        self.menu_items = menu_items

        self.draw_title_bar()
    
    def draw_title_bar(self):
        """draw the title bar at the top of the window"""
        self.title_win.clear() # Clear any Previous Content

        # Setting up Variables
        win_max_h, win_max_w = self.title_win.getmaxyx()
        title_text = f"┨ {self.title} ┠"
        decoration_left = "╭────"
        decoration_right = "────╮"
        filler = "─"

        # Calculate spacing
        total_decoration = len(decoration_left) + len(decoration_right) + len(title_text)
        remaining = win_max_w - total_decoration

        if remaining > 0:
            # Center the title
            filler_left = filler * (remaining // 2)
            filler_right = filler * (remaining - remaining // 2)
            title_bar = f"{decoration_left}{filler_left}{title_text}{filler_right}{decoration_right}"
        else:
            # Fallback if window is too narrow
            title_bar = f"{self.title[:win_max_w]}"#{decoration_left}{title_text}{filler_right}"
        
        # insstr because add string has trouble inserting at bottom right corner of display
        self.title_win.insstr(0, 0, title_bar[:win_max_w], curses.A_BOLD)
        self.title_win.refresh()

class TitleBar:
    def __init__(self, stdscr, title):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()
        self.win = curses.newwin(1, max_w, 0,0) # One Line Tall, Across whole Terminal, Top-left of page
        self.title = title

    def draw_title_bar(self):
        """draw the title bar at the top of the window"""
        self.win.clear() # Clear any Previous Content

        # Setting up Variables
        win_max_h, win_max_w = self.win.getmaxyx()
        title_text = f"┨ {self.title} ┠"
        decoration_left = "╭────"
        decoration_right = "────╮"
        filler = "─"

        # Calculate spacing
        total_decoration = len(decoration_left) + len(decoration_right) + len(title_text)
        remaining = win_max_w - total_decoration

        if remaining > 0:
            # Center the title
            filler_left = filler * (remaining // 2)
            filler_right = filler * (remaining - remaining // 2)
            title_bar = f"{decoration_left}{filler_left}{title_text}{filler_right}{decoration_right}"
        else:
            # Fallback if window is too narrow
            title_bar = f"{self.title[:win_max_w]}"#{decoration_left}{title_text}{filler_right}"
        
        # insstr because add string has trouble inserting at bottom right corner of display
        self.win.insstr(0, 0, title_bar[:win_max_w], curses.A_BOLD)
        self.win.refresh()

    def cleanup(self):
        """clear & refresh the window to safely destroy it"""
        self.win.clear()
        self.win.refresh()
        del self.win


class PagesBar:
    def __init__(self, stdscr, menu_items, selected=0):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()
        self.win = curses.newwin(1, max_w, 1,0) # One Line Tall, Across whole Terminal, Below the Title Bar, with Text elements Conncting
        
        self.menu_items = menu_items
        
    def draw_pages_bar(self, selected):
        """
        
        :Output: ╰─┄ 1. scripts ┄─┄ 2. Graph View ┄─┄ 3. Tests ┄─────╯
        """
        self.win.clear()
        win_max_h, win_max_w = self.win.getmaxyx()

        # Create menu parts
        decoration_left = "╰──┄"
        menu_joiner = " ┄─┄ "
        filler = "─"
        filler_start = "┄"
        filler_end = "╯"

        # Assemble menu parts
        menu_parts = []
        for i, item in enumerate(self.menu_items):
            menu_parts.append((i, f"{i + 1}. {item}"))
        menu_text = menu_joiner.join([text for _, text in menu_parts])
        menu_content = f" {menu_text} "

        # calculate length for the right side filler
        filler_avail = win_max_w - len(decoration_left) - len(menu_content) - len(filler_end) - len(filler_start)
        remaining = win_max_w-2 - len(decoration_left) - len(menu_text) - len(filler_start) - len(filler_end)
        
        # when no space for decorations is availabile drop it
        if remaining > 0: fill = filler_start + filler * filler_avail + filler_end
        else: fill = ""
        # Assemble Full menu Bar
        menu_bar_text = f"{decoration_left}{menu_text}{fill}"


        # Left Edge Decorator plus whitespace before menu items
        col = 0
        self.win.addstr(0, col, decoration_left)
        col += len(decoration_left)
        self.win.addstr(0, col, " ")
        col += 1
        # Draw each menu item with highlighting currently selected
        for i, (idx, item_txt) in enumerate(menu_parts):
            if idx == selected:
                self.win.insstr(0, col, item_txt, curses.A_REVERSE)
            else:
                self.win.addstr(0, col, item_txt)
            col += len(item_txt)
            if i < len(menu_parts) - 1:
                self.win.addstr(0, col, menu_joiner)
                col += len(menu_joiner)
        # Whitespace after menu items
        self.win.addstr(0, col, " ")
        col += 1
        # Right Edge Decorator
        self.win.insstr(0, col, fill)
        self.win.refresh()
    
    def cleanup(self):
        """clear & refresh the window to safely destroy it"""
        self.win.clear()
        self.win.refresh()
        del self.win    

def main(stdscr):
    
    title = "Tramrunner"
    menu_items = ["Scripts", "Graph View", "Tests"]
    selected = 0
    #menu = MenuWindow(stdscr, menu_items, None, 0, 0, 0)
    #menu.title = "Tramrunner"
    #menu.move(10, 0)
    #menu.render_w_border()
    stdscr.clear()
    stdscr.refresh()
    title_bar = TitleBar(stdscr, title)
    title_bar.draw_title_bar()
    pages_bar = PagesBar(stdscr, menu_items)
    pages_bar.draw_pages_bar(selected)
    
    
    #title_bar.win.refresh()
    while True:

        height, width = stdscr.getmaxyx()
        #stdscr.addstr(4, 2, f"Current page: {menu_items[selected]}")
        #stdscr.addstr(6, 2, "Press 1-3 to switch pages, 'q' to quit")
        pages_bar.draw_pages_bar(selected)
        pages_bar.win.refresh()
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('1'):
            selected = 0
        elif key == ord('2'):
            selected = 1
        elif key == ord('3'):
            selected = 2
        #title_bar.win.refresh()

if __name__  == "__main__":
    curses.wrapper(main)