import curses
import time
#import stop_info_tui
import header
import screen


def main(stdscr):
    # clear and refresh the screen (also kinda 'initiates' the screen) --> lesson learned
    stdscr.clear()
    stdscr.refresh()

    title = "Tramrunner"
    page_titles = ["Scripts", "Graph View", "Tests"]
    page_select = 0
    page_menus = [
        ["Stop info","Query Trip", "Opt3"],
        ["display menu1"], 
        ["testies.py"]  
    ]
    menu_item_select = 0

    title_bar = header.TitleBar(stdscr, title)
    title_bar.draw_title_bar()
    pages_bar = header.PagesBar(stdscr, page_titles)
    pages_bar.draw_pages_bar(page_select)



   

    while True:

        # Handle input
        key = stdscr.getch()
        
        if key == ord('q') or key == ord('Q'):
            break
        # select pages
        elif key in [ord('1'), ord('2'), ord('3')]:
            page_select = int(chr(key)) - 1
            pages_bar.draw_pages_bar(page_select)
        # menu item selection keys
        elif key == curses.KEY_UP and menu_item_select > 0:
            menu_item_select -= 1
        elif key == curses.KEY_DOWN and menu_item_select < len(page_menus[page_select]) - 1:
            menu_item_select += 1   
    

if __name__ == "__main__":
    #stop_info_tui.stop_info_tui("rac")
    curses.wrapper(main)