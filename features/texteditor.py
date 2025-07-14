import curses
import pyfiglet
import time

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 8
        self.cursor_position = 0
        self.length = [""]
        self.line_types = ["soft"]  # track line source
        self.height, self.width = self.stdscr.getmaxyx()
        self.prev_line_count = 1

    def run(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.scrollok(True)

        while True:
            message = pyfiglet.figlet_format("TextEditor", font="slant")
            self.stdscr.addstr(0, 1, message)
            self.stdscr.addstr(6, 2, "     ---------------------------      ")
            self.redraw_text()
            self.movement()
            if self.current_line == self.height - 2:
                self.new_line()

            key = self.stdscr.getch()
            if self.handle_input(key):
                break

            self.automation()
            self.stdscr.refresh()

    def display_text(self):

        for i in range(len(self.length)):
            for char in (self.length[i]):
                self.stdscr.addstr(self.current_line, self.cursor_position, char)

    def handle_input(self, key):
        if key == 27:
            return True
        
        elif key in (10, curses.KEY_ENTER):
            self.enter()

        elif key in (127, curses.KEY_BACKSPACE):
            self.remove()

        elif key == 6:
            self.save_file()

        elif key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            self.arrows(key)

        else:
            if self.cursor_position + 2 == self.width:
                self.length.append("")
                self.line_types.append("soft")
                self.current_line += 1
                self.cursor_position = 0

            if len(self.length[self.current_line - 8]) > 0:
                self.length[self.current_line - 8] = self.length[self.current_line - 8][:self.cursor_position] + chr(key) + self.length[self.current_line - 8][self.cursor_position:]

            else:
                self.length[self.current_line - 8] += chr(key)

            self.cursor_position += 1
            self.redraw_text()

        # Show position
        self.stdscr.move(self.height - 1, 0)
        self.stdscr.clrtoeol()
        position = f"Row: {self.current_line - 7}, Col: {self.cursor_position + 1}"
        self.stdscr.addstr(self.height - 1, self.width // 2 - len(position) // 2, position, curses.A_BOLD)
        self.stdscr.refresh()
        self.movement()

    def remove(self):
        line_index = self.current_line - 8

        if self.cursor_position == 0:
            if self.current_line == 8 and len(self.length[line_index]) == 0:
                pass
            
            if line_index > 0:
                self.cursor_position = len(self.length[line_index - 1])
                self.length[line_index - 1] += self.length[line_index]
                self.length.pop(line_index)
                self.line_types.pop(line_index)
                self.current_line -= 1
        else:
            line = self.length[line_index]
            self.length[line_index] = line[:self.cursor_position - 1] + line[self.cursor_position:]
            self.cursor_position -= 1

            # Shift characters up from next line only if it was soft-wrapped
            i = line_index
            while i + 1 < len(self.length):
                if (self.line_types[i + 1] == "soft" and
                    len(self.length[i]) < self.width - 2 and
                    len(self.length[i + 1]) > 0):
                    self.length[i] += self.length[i + 1][0]
                    self.length[i + 1] = self.length[i + 1][1:]
                    i += 1
                else:
                    break

            # Remove empty soft lines
            i = 0
            while i < len(self.length):
                if i < len(self.line_types) and self.length[i] == "" and self.line_types[i] == "soft":
                    self.length.pop(i)
                    self.line_types.pop(i)
                else:
                    i += 1

        self.redraw_text()
        self.movement()

    def redraw_text(self):
        current_line_count = len(self.length)
        text_start_line = 8
        for i in range(max(self.prev_line_count, current_line_count)):
            self.stdscr.move(text_start_line + i, 0)
            self.stdscr.clrtoeol()
            if i < current_line_count:
                line = self.length[i]
                padded_line = line + " " * (self.width - len(line) - 1)
                self.stdscr.addstr(8 + i, 1, padded_line[:self.width - 1])
        self.prev_line_count = current_line_count

    def enter(self):
        self.length.append("")

        if len(self.length[self.current_line - 8][self.cursor_position:]) > 0:
            new_len = len(self.length[(self.current_line - 8):])
            for index in range(new_len -1, 0, -1):
                self.length[self.current_line - 8 + index] = self.length[self.current_line - 8 + index - 1]

            self.length[self.current_line - 8 + 1] = self.length[self.current_line - 8][self.cursor_position:]
            self.length[self.current_line - 8] = self.length[self.current_line - 8][:self.cursor_position]
            self.line_types.append("hard")
            

        self.line_types.append("hard")
        self.current_line += 1
        self.cursor_position = 0
        self.redraw_text()

    def save_file(self):

        with open("file.txt", "w") as file:
            counter = 0
            for line in self.length:
                self.text += line
                counter += 1
                if counter != len(self.length):
                    self.text += "\n"
            file.write(self.text)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.stdscr.addstr(self.height - 2, 0, "File has been saved!", curses.color_pair(1))
        self.stdscr.refresh()
        time.sleep(1.5)
        self.stdscr.move(self.height - 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

    def open_file(self):
        pass

    def arrows(self, key):

        if key == curses.KEY_UP:
            if self.current_line > 8:
                self.current_line -= 1
                self.cursor_position = min(self.cursor_position, len(self.length[self.current_line - 8]))
                self.movement()

        elif key == curses.KEY_DOWN:
            if self.current_line - 8 < len(self.length) - 1:
                self.current_line += 1
                self.cursor_position = min(self.cursor_position, len(self.length[self.current_line - 8]))
                self.movement()

        elif key == curses.KEY_LEFT:
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.movement()

            elif self.current_line > 8:
                self.current_line -= 1
                self.cursor_position = len(self.length[self.current_line - 8])
                self.movement()

        elif key == curses.KEY_RIGHT:
            line_len = len(self.length[self.current_line - 8])

            if self.cursor_position < line_len:
                self.cursor_position += 1
                self.movement()

            elif self.current_line - 8 < len(self.length) - 1:
                self.current_line += 1
                self.cursor_position = 0
                self.movement()

    def movement(self):
        self.stdscr.move(self.current_line, self.cursor_position + 1)


    def automation(self):
        if len(self.length) == 0:
            self.length = [""]

    def new_line(self):
        self.stdscr.resize(self.height + 1, self.width)
        self.height, self.width = self.stdscr.getmaxyx()
        self.stdscr.clear()
        self.redraw_text()
        self.cursor_position = 0
        self.current_line = len(self.length) + 7
        self.movement()
        self.stdscr.refresh()


