class PageSubMenu:
    def __init__(self, stdscr, page_menus: list):
        self.stdscr = stdscr
        max_h, max_w = self.stdscr.getmaxyx()
        menu_width = 0
        # calculate menu width
        for item in page_menus:
            menu_width = max(menu_width, len(max(item, key=len)))
        self.win = curses.newwin(10, 10, 10, 10,) # One Line Tall, minimum menu width to accomedate all items without overflow, Top of page
        self.page_menus = page_menus

    def render_sub_menu(self, page_menus, selected):
        self.win.clear()
        self.win.box()
        self.win.addstr(1, 1, "Pos1")
        self.win.refresh()