import curses


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
        """
        ╭───────────────────┨ Tramrunner ┠───────────────────╮  -- Window title bar
        ╰─┄ 1. scripts ┄─┄ 2. Graph View ┄─┄ 3. Tests ┄──────╯  -- window pages bar
        ╭────────────────────────────────────────────────────╮  -- window page sub menu
        │                                                    │  -- window content
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        │                                                    │
        ╰────────────────────────────────────────────────────╯
        """

        max_y, max_x = self.stdscr.getmaxyx()
        left_width = max_x // 3
        menu_width = max_x // 5

        #self.submenu_panel = curses.newwin(max_y - 6 , menu_width, 4, 0)
        #self.script_window = curses.newwin(max_y - 6, max_x - menu_width, 4, menu_width)


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



    def draw_script_window(self, content_lines):
        self.script_window.clear()
        self.script_window.box()
        self.script_window.addstr(0, 2, " Script Window ", curses.A_BOLD)
        
        max_y, max_x = self.script_window.getmaxyx()
        
        for idx, line in enumerate(content_lines):
            if idx + 1 >= max_y - 1:  # Leave room for border
                break
            safe_line = line[:max_x - 3]  # Truncate if needed
            self.script_window.addstr(idx + 1, 1, safe_line)
        
        self.script_window.refresh()

    def run(self):


        self.stdscr.nodelay(False)
        
        self.stdscr.refresh()


    def handle_selection(self, selection, page_select):

        """Simulate processing based on menu selection"""
        if page_select == 0:
            if selection == 0:return[f"Print Stop Info Here"]
            elif selection == 1:return[f"Query Trip Info"]
            elif selection == 2:return[f"Tja was soll hier hin?"]                                     
        elif page_select == 1:
            if selection == 0:return[f"Testies.py"]
            elif selection == 1:return[f"HEllO from handle_selection"]
        return []

class InfoScreen:
    def __init__(self, stdscr, page_menus):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()
        #Calculate the menu width again???
        menu_width = 0
        for item in page_menus:
            menu_width = max(menu_width, len(max(item, key=len)))+1 # Ach keine ahnung + 3 # Same as belo, again why are we doing this again?
        self.win = curses.newwin(max_h - 2, max_w - menu_width, 2, menu_width,)

    def render_stop_info1(self, stop_info: list):
        self.win.clear()
        self.win.box()
        out_line = 2
        for entry in stop_info:
            out_line += 1 

            printer = f"[{entry.get('time_scheduled')}] [{entry.get('time_relative')}] -{entry.get('nr')}-> {entry.get('direction')}{entry.get('mot')}"
            
            self.win.addstr(out_line, 1, printer)
        self.win.refresh()


class PageSubMenu:
    def __init__(self, stdscr, page_menus: list):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()
        menu_width = 0
        # calculate menu width
        for item in page_menus:
            menu_width = max(menu_width, len(max(item, key=len))) + 1 # Off by one + 2 offset down below menu spacing
        self.win = curses.newwin(max_h - 2, menu_width, 2, 0,) # One Line Tall, minimum menu width to accomedate all items without overflow, Top of page
        self.page_menus = page_menus

    def render_sub_menu(self, menu_items, selected):
        self.win.clear()
        self.win.box()
        for idx, item in enumerate(menu_items):
            y = idx + 2
            if idx == selected:
                self.win.addstr(y, 0, f"├─{item}", curses.A_REVERSE)
            else:
                self.win.addstr(y, 0, f"│ {item}")
        self.win.refresh()