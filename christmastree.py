import curses
import time
import random
import logging

logging.basicConfig(
    filename='christmastree.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ChristmasTreeDisplay:
    def __init__(self, tree_lines, color_pairs, stdscr):
        self.tree_lines = tree_lines
        self.color_pairs = color_pairs
        self.stdscr = stdscr
        self.light_states = {}
        self.min_delay = 0.5
        self.max_delay = 2.0
        self.initialize_lights()

    def initialize_lights(self):
        current_time = time.time()
        for line_idx, line in enumerate(self.tree_lines):
            for char_idx, char in enumerate(line):
                if char == 'O':
                    color = random.choice(self.color_pairs)
                    next_change = current_time + random.uniform(self.min_delay, self.max_delay)
                    self.light_states[(line_idx, char_idx)] = {'color': color, 'next_change': next_change}

    def update_lights(self):
        current_time = time.time()
        for position, state in self.light_states.items():
            if current_time >= state['next_change']:
                available_colors = [cp for cp in self.color_pairs if cp != state['color']]
                if not available_colors:
                    available_colors = self.color_pairs
                new_color = random.choice(available_colors)
                self.light_states[position]['color'] = new_color
                self.light_states[position]['next_change'] = current_time + random.uniform(self.min_delay, self.max_delay)

    def draw_tree(self):
        max_y, max_x = self.stdscr.getmaxyx()
        try:
            for x in range(max_x):
                self.stdscr.addch(0, x, '-', curses.color_pair(4))
                self.stdscr.addch(max_y - 1, x, '-', curses.color_pair(4))
            for y in range(max_y):
                self.stdscr.addch(y, 0, '|', curses.color_pair(4))
                self.stdscr.addch(y, max_x - 1, '|', curses.color_pair(4))
            self.stdscr.addch(0, 0, '+', curses.color_pair(4))
            self.stdscr.addch(0, max_x - 1, '+', curses.color_pair(4))
            self.stdscr.addch(max_y - 1, 0, '+', curses.color_pair(4))
            self.stdscr.addch(max_y - 1, max_x - 1, '+', curses.color_pair(4))
        except curses.error:
            pass
        tree_width = max(len(line) for line in self.tree_lines)
        start_x = (max_x - tree_width) // 2
        for line_idx, line in enumerate(self.tree_lines):
            if line_idx + 1 >= max_y - 1:
                break
            for char_idx, char in enumerate(line):
                x_position = start_x + char_idx
                y_position = line_idx + 1
                if 0 <= x_position < max_x - 1 and 0 <= y_position < max_y - 1:
                    if char == '★':
                        self.stdscr.addstr(y_position, x_position, char, curses.color_pair(7) | curses.A_BOLD)
                    elif char == 'O':
                        color = self.light_states.get((line_idx, char_idx), {}).get('color', curses.color_pair(7))
                        self.stdscr.addstr(y_position, x_position, char, color)
                    elif char == '*':
                        self.stdscr.addstr(y_position, x_position, char, curses.color_pair(2))
                    else:
                        self.stdscr.addstr(y_position, x_position, char, curses.color_pair(7))
        self.stdscr.noutrefresh()

    def update_display(self):
        self.update_lights()
        self.draw_tree()

def christmas_tree_app(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    curses.init_pair(4, curses.COLOR_BLUE, -1)
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)
    curses.init_pair(6, curses.COLOR_CYAN, -1)
    curses.init_pair(7, curses.COLOR_WHITE, -1)
    tree_lines = [
        "        ★        ",
        "        *        ",
        "       ***       ",
        "      *O*O*      ",
        "     *******     ",
        "    *O*****O*    ",
        "   ***********   ",
        "  *O*********O*  ",
        "       ***       ",
        "       ***       "
    ]
    tree_display = ChristmasTreeDisplay(
        tree_lines=tree_lines,
        color_pairs=[curses.color_pair(1), curses.color_pair(2),
                    curses.color_pair(3), curses.color_pair(5),
                    curses.color_pair(6)],
        stdscr=stdscr
    )
    while True:
        try:
            stdscr.clear()
            max_y, max_x = stdscr.getmaxyx()
            if max_y < 20 or max_x < 40:
                stdscr.addstr(max_y//2, max(0, (max_x - 30)//2), "Terminal muito pequeno.", curses.color_pair(1))
                stdscr.refresh()
                time.sleep(1)
                continue
            tree_display.update_display()
            stdscr.refresh()
            key = stdscr.getch()
            if key != -1:
                break
            time.sleep(0.1)
        except Exception as e:
            logging.exception("Erro na aplicação da árvore de natal.")
            break
    curses.endwin()

if __name__ == "__main__":
    try:
        curses.wrapper(christmas_tree_app)
    except Exception as e:
        logging.exception("Erro na execução principal.")
        print("Ocorreu um erro. Verifique o arquivo christmastree.log para mais detalhes.")

