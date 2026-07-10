import curses

class boilerplate_curses:
    def __init__ (self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(1) #Show Cursor

        # Call functions to Setup enviroment
        # eg:
        # self.setup_colors()
        # self setup_create_windows()

    def run(self):
        page_title = "Boilerplate"
        sample_text = "Press Q to Quit"

        self .stdscr.clear()
        self.stdscr.box()
        self.stdscr.addstr(0, 0, sample_text)
        self.stdscr.refresh()
        while True:


            key = self.stdscr.getch()
            if key == ord('q') or key == ord('Q'):
                break

def main(stdscr):
    app = boilerplate_curses(stdscr)
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)