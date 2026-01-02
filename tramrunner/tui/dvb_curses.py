import curses
import time
#import stop_info_tui
import header

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
        ╭───────────────────┨ Tramrunner ┠───────────────────╮
        ╰─┄ 1. scripts ┄─┄ 2. Graph View ┄─┄ 3. Tests ┄──────╯
        ╭────────────────────────────────────────────────────╮
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
        │                                                    │
        ╰────────────────────────────────────────────────────╯
        """

        max_y, max_x = self.stdscr.getmaxyx()
        left_width = max_x // 3
        menu_width = max_x // 5

        self.left_panel = curses.newwin(max_y - 6 , menu_width, 4, 0)
        self.script_window = curses.newwin(max_y - 6, max_x - menu_width, 4, menu_width)
        #self.header = curses.newwin(3, max_x, 0, 0)
        #self.right_panel = curses.newwin(max_y - 6, max_x - menu_width, 3, menu_width)
        #self.status = curses.newwin(3, max_x, max_y - 3, 0)


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

def main(stdscr):
    title = "Tramrunner"
    page_titles = ["Scripts", "Graph View", "Tests"]
    page_select = 0
    page_menus = [
        ["Stop info","Query Trip", "Opt3"],
        ["display menu1"], 
        ["testies.py", "SayHi!", "Opt3"]  
    ]
    menu_item_select = 0

    app = dvb_curse(stdscr)
    app.run()
    title_bar = header.TitleBar(stdscr, title)
    title_bar.draw_title_bar()
    pages_bar = header.PagesBar(stdscr, page_titles)
    pages_bar.draw_pages_bar(page_select)
    

    while True:

        height, width = stdscr.getmaxyx()
        #stdscr.addstr(4, 2, f"Current page: {menu_items[selected]}")
        #stdscr.addstr(6, 2, "Press 1-3 to switch pages, 'q' to quit")
        pages_bar.draw_pages_bar(page_select)
        pages_bar.win.refresh()
        app.draw_left_panel(page_menus[page_select], page_select)
        stdscr.refresh()
        
        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break
        
        # select pages
        elif key == ord('1'):
            page_select = 0
        elif key == ord('2'):
            page_select = 1
        elif key == ord('3'):
            page_select = 2
        # menu item selection keys
        elif key == curses.KEY_UP and menu_item_select > 0:
            menu_item_select -= 1
        elif key == curses.KEY_DOWN and menu_item_select < len(page_menus[page_select]) - 1:
            menu_item_select += 1
        #title_bar.win.refresh()    
    

if __name__ == "__main__":
    #stop_info_tui.stop_info_tui("rac")
    curses.wrapper(main)