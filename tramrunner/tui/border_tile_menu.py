import curses

def draw_bordered_menu(stdscr, current_row, menu_items):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Calculate box dimensions
    box_height = len(menu_items) + 4
    box_width = max(len(item) for item in menu_items) + 10
    start_y = h//2 - box_height//2
    start_x = w//2 - box_width//2
    
    # Draw border
    stdscr.attron(curses.color_pair(1))
    for i in range(box_height):
        for j in range(box_width):
            if i == 0 or i == box_height - 1:
                stdscr.addstr(start_y + i, start_x + j, "═")
            elif j == 0 or j == box_width - 1:
                stdscr.addstr(start_y + i, start_x + j, "║")
    
    # Draw corners
    stdscr.addstr(start_y, start_x, "╔")
    stdscr.addstr(start_y, start_x + box_width - 1, "╗")
    stdscr.addstr(start_y + box_height - 1, start_x, "╚")
    stdscr.addstr(start_y + box_height - 1, start_x + box_width - 1, "╝")
    stdscr.attroff(curses.color_pair(1))
    
    # Draw title
    title = " MAIN MENU "
    stdscr.addstr(start_y, start_x + box_width//2 - len(title)//2, title, 
                  curses.color_pair(2) | curses.A_BOLD)
    
    # Draw menu items
    for idx, item in enumerate(menu_items):
        y = start_y + 2 + idx
        x = start_x + box_width//2 - len(item)//2
        
        if idx == current_row:
            stdscr.addstr(y, x - 2, "▶", curses.color_pair(3))
            stdscr.addstr(y, x, item, curses.color_pair(3) | curses.A_BOLD)
        else:
            stdscr.addstr(y, x, item, curses.color_pair(1))
    
    # Draw footer
    footer = "↑/↓: Navigate | Enter: Select | q: Quit"
    stdscr.addstr(h - 2, w//2 - len(footer)//2, footer, curses.A_DIM)
    
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    menu_items = ["New Game", "Load Game", "Settings", "Credits", "Exit"]
    current_row = 0
    
    while True:
        draw_bordered_menu(stdscr, current_row, menu_items)
        key = stdscr.getch()
        
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu_items) - 1:
            current_row += 1
        elif key == ord('\n'):
            if current_row == len(menu_items) - 1:
                break
            stdscr.addstr(0, 0, f"You selected: {menu_items[current_row]}")
            stdscr.refresh()
            stdscr.getch()
        elif key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)