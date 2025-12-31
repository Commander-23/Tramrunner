import curses
import time
#import stop_info_tui

class dvb_curse:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0) # Hide Curser
        self.setup_colors()
        self.create_windows()
       #def draw_header(self, title):
        #    self.header.clear()
        #    self.header.box()
        #
        #    # Center the title
        #    max_y, max_x = self.header.getmaxyx()
        #    x = (max_x - len(title)) // 2
        #    self.header.addstr(1, x, title, curses.color_pair(1) | curses.A_BOLD)
        #    self.header.refresh()

        #def draw_status(self, message):
        #    self.status.clear()
        #    self.status.box()
        #    self.status.addstr(1, 2, message, curses.color_pair(2))
        #    self.status.refresh()

    def setup_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    def create_windows(self):
        """
        ######### Title Line ##########
        +-----------------------------+
        | Header                      |
        +-------------+---------------+
        | Menu        | Output        |
        |             |               |
        |             |               |
        |             |               |
        +-------------+---------------+
        """

        max_y, max_x = self.stdscr.getmaxyx()
        left_width = max_x // 3
        menu_width = max_x // 5
        
        self.title_line = curses.newwin(1, max_x, 0, 0)
        self.pages_bar = curses.newwin(3, max_x, 1, 0)
        self.left_panel = curses.newwin(max_y - 6 , menu_width, 4, 0)
        self.script_window = curses.newwin(max_y - 6, max_x - menu_width, 4, menu_width)
        #self.header = curses.newwin(3, max_x, 0, 0)
        #self.right_panel = curses.newwin(max_y - 6, max_x - menu_width, 3, menu_width)
        #self.status = curses.newwin(3, max_x, max_y - 3, 0)

    def draw_title_line(self, title_str):
        self.title_line.clear()
        self.title_line.box()
        self.title_line.addstr(0, 0, title_str)
        self.title_line.refresh()

    def draw_pages_bar(self, page_title, page_selected):
        self.pages_bar.clear()
        self.pages_bar.box()
        self.pages_bar.addstr(1, 4, " Pages Bar ", curses.A_BOLD)
        self.pages_bar.addstr(2, 0, page_title[page_selected])
        self.pages_bar.refresh()

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

        page_title = ["[1]-Run Scripts", "[2]-Test Scripts", "[3]-Display Experiments"]
        page_menus = [
            ["Stop info","Query Trip", "Opt3"],
            ["testies.py", "SayHi!", "Opt3"], 
            ["display_menu1"]  
        ]
        page_select = 0
        selected = 0
        content = ["Welcome! Select an option from the menu."]
        
        self.draw_title_line("### Title ###")
        self.draw_pages_bar(page_title, page_select)
        
        self.stdscr.nodelay(False)
        
        self.stdscr.refresh()
        while True:
            self.draw_pages_bar(page_title, page_select)
            self.draw_left_panel(page_menus[page_select], selected)
            self.draw_script_window(content)
            key = self.stdscr.getch()
            
            if key == ord('1'):
                page_select = 0
                selected = 0
            elif key == ord('2'):
                page_select = 1
                selected = 0
            elif key == ord('3'):
                page_select = 2
                selected = 0
            elif key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(page_menus[page_select]) - 1:
                selected += 1
            elif key == ord('\n'):
                    content = self.handle_selection(selected, page_select)
            elif key == ord('q') or key == ord('Q'): # Quit
                break
                
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
    app = dvb_curse(stdscr)
    app.run()

if __name__ == "__main__":
    #stop_info_tui.stop_info_tui("rac")
    curses.wrapper(main)