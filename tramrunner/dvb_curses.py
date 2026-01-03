import curses
import time
from stop_info_tui import stop_info_tui
import tui



def main(stdscr):
    # clear and refresh the screen (also kinda 'initiates' the screen) --> lesson learned
    stdscr.clear()
    stdscr.refresh()

    title = "Tramrunner"
    page_titles = ["Scripts", "Input", "Graph View"]
    page_select = 0
    page_menus = [
        ["Stop info","Query Trip", "Opt3"],
        ["text:test"], 
        ["soooooo.py"]  
    ]
    menu_item_select = 0

    title_bar = tui.TitleBar(stdscr, title)
    title_bar.draw_title_bar()
    pages_bar = tui.PagesBar(stdscr, page_titles)
    pages_bar.draw_pages_bar(page_select)
    sub_menu = tui.PageSubMenu(stdscr, page_menus)
    sub_menu.render_sub_menu(page_menus[page_select], menu_item_select)
    info_screen = tui.InfoScreen(stdscr, page_menus)
    info_screen.render_stop_info1(stop_info_tui("rac"))
    while True:

        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break

        # select pages and move page if needed
        elif key in [ord('1'), ord('2'), ord('3')]:
            page_select = int(chr(key)) - 1
            if menu_item_select >= len(page_menus[page_select]):
                menu_item_select = len(page_menus[page_select])-1
            pages_bar.draw_pages_bar(page_select)
            sub_menu.render_sub_menu(page_menus[page_select], menu_item_select)

        # menu item selection keys
        elif key == curses.KEY_UP and menu_item_select > 0:
            menu_item_select -= 1
            pages_bar.draw_pages_bar(page_select)
            sub_menu.render_sub_menu(page_menus[page_select], menu_item_select)
        elif key == curses.KEY_DOWN and menu_item_select < len(page_menus[page_select]) - 1:
            menu_item_select += 1
            pages_bar.draw_pages_bar(page_select)
            sub_menu.render_sub_menu(page_menus[page_select], menu_item_select)


if __name__ == "__main__":
    curses.wrapper(main)