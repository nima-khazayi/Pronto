import curses
import pyfiglet
import time

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 0
        self.cursor_position = 0
        self.length = [""]
        self.line_types = ["soft"]  # track line source
        self.height, self.width = self.stdscr.getmaxyx()
        self.prev_line_count = 1

    # Main running function
    def run(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.scrollok(True)

        while True:
            message = pyfiglet.figlet_format("TextEditor", font="slant")
            self.stdscr.addstr(0, 1, message)
            self.stdscr.addstr(6, 2, "     ---------------------------      ")
            self.shift_text()
            self.movement()
            
            key = self.stdscr.getch()
            if self.handle_input(key):
                break

            self.automation()
            self.stdscr.refresh()

    # Displaying function
    def display_text(self, string=None):
        if string is None:
            string = self.length

        for i in range(len(string)):
            for char in (string[i]):
                self.stdscr.addstr(self.current_line, self.cursor_position, char)

    # Function to handle key inputs
    def handle_input(self, key):
        if key == 27:
            return True
        
        elif key in (10, curses.KEY_ENTER):
            self.enter()

        elif key in (127, curses.KEY_BACKSPACE):
            self.remove()

        elif key == 6:
            self.save_file()

        elif key == 9:
            self.cursor_position += 4
            self.length[self.current_line] += "    "
            self.movement()

        elif key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            self.arrows(key)

        else:   
            if len(self.length[self.current_line][self.cursor_position:]) > 0:
                if len(self.length[self.current_line]) + 2 >= self.width:
                    # We should check if we are at last line or not,
                    # if not we should check if the next line has enough space or not,
                    # if not then check if it's soft or not
                    # if not create another empty line
                    self.length.append("")
                    self.line_types.append("soft")
                    self.length[-1] += self.length[-2][-1]
                    self.length[-2] = self.length[-2][:-1]
                self.length[self.current_line] = self.length[self.current_line][:self.cursor_position] + chr(key) + self.length[self.current_line][self.cursor_position:]

            else:
                if self.cursor_position + 2 >= self.width:
                    self.length.append("")
                    self.line_types.append("soft")
                    self.current_line += 1
                    self.cursor_position = 0
                self.length[self.current_line] += chr(key)

            self.cursor_position += 1
            self.shift_text()
            self.movement()

        # Show position
        self.stdscr.move(self.height - 1, 0)
        self.stdscr.clrtoeol()
        position = f"Row: {self.current_line + 1}, Col: {self.cursor_position + 1}"
        self.stdscr.addstr(self.height - 1, self.width // 2 - len(position) // 2, position, curses.A_BOLD)
        self.stdscr.refresh()
        self.movement()

    # Removing function using backspace
    def remove(self):
        line_index = self.current_line

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

        self.shift_text()
        self.movement()

    # Function to redraw the whole page
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

    # Entering function, new lines and even spliting lines
    def enter(self):
        self.length.append("")

        if len(self.length[self.current_line][self.cursor_position:]) > 0:
            new_len = len(self.length[(self.current_line):])
            for index in range(new_len -1, 0, -1):
                self.length[self.current_line + index] = self.length[self.current_line + index - 1]

            self.length[self.current_line + 1] = self.length[self.current_line][self.cursor_position:]
            self.length[self.current_line] = self.length[self.current_line][:self.cursor_position]
            self.line_types.append("hard")
            

        self.line_types.append("hard")
        if self.current_line == self.height - 3:
            self.current_line = len(self.length) - 1  # buffer index

        else:
            self.current_line += 1

        self.cursor_position = 0
        self.shift_text()
        self.movement()
        self.stdscr.refresh()

    # Moving around the text file
    def arrows(self, key):
        if key == curses.KEY_UP:
            if self.current_line > 8:
                self.current_line -= 1
                self.cursor_position = min(self.cursor_position, len(self.length[self.current_line]))
                

        elif key == curses.KEY_DOWN:
            if self.current_line < len(self.length) - 1:
                self.current_line += 1
                self.cursor_position = min(self.cursor_position, len(self.length[self.current_line]))
                

        elif key == curses.KEY_LEFT:
            if self.cursor_position > 0:
                self.cursor_position -= 1
                

            elif self.current_line > 8:
                self.current_line -= 1
                self.cursor_position = len(self.length[self.current_line])
                

        elif key == curses.KEY_RIGHT:
            line_len = len(self.length[self.current_line])

            if self.cursor_position < line_len:
                self.cursor_position += 1
            

            elif self.current_line < len(self.length) - 1:
                self.current_line += 1
                self.cursor_position = 0
                
        self.shift_text()
        self.movement()

    # Always should be in the right place to type
    def movement(self):
        self.height, self.width = self.stdscr.getmaxyx()
        text_start_line = 8
        text_end_line = self.height - 3
        visible_lines = text_end_line - text_start_line

        total_lines = len(self.length)
        start_index = max(0, total_lines - visible_lines)

        # Convert current_line (buffer index) to screen position
        screen_line = text_start_line + (self.current_line - start_index)
        screen_line = min(max(screen_line, text_start_line), text_end_line - 1)

        cursor_x = min(self.cursor_position + 1, self.width - 2)
        self.stdscr.move(screen_line, cursor_x)

    # Just for arrows
    def cursor(self):
        self.stdscr.move(self.current_line, self.cursor_position + 1)

    # Never let the text gets empty
    def automation(self):
        if len(self.length) == 0:
            self.length = [""]
            self.line_types = ["soft"]  # track line source

    # When the page size has finished scroll up
    def shift_text(self):
        self.height, self.width = self.stdscr.getmaxyx()
        text_start_line = 8
        text_end_line = self.height - 3
        visible_lines = text_end_line - text_start_line

        total_lines = len(self.length)
        start_index = max(0, total_lines - visible_lines)

        # Clear visible area
        for i in range(visible_lines):
            screen_line = text_start_line + i
            self.stdscr.move(screen_line, 0)
            self.stdscr.clrtoeol()

            if start_index + i < total_lines:
                line = self.length[start_index + i]
                self.stdscr.addstr(screen_line, 1, line[:self.width - 2])

        # Adjust current_line to stay within visible range
        # self.current_line = len(self.length) - 1
        self.prev_line_count = total_lines

    # We should finally save the text file in any extension
    def save_file(self):

        try:
            filename = ""
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            self.stdscr.addstr(self.height - 2, 0, "Enter your file name -> ", curses.color_pair(1))
            self.stdscr.move(self.height - 2, 24)
            while True:
                key = self.stdscr.getch()
                
                if key in (10, curses.KEY_ENTER):
                    with open(filename, "w") as file:
                        counter = 0
                        for line in self.length:
                            self.text += line
                            counter += 1
                            if counter != len(self.length):
                                self.text += "\n"
                        file.write(self.text)
                        break

                elif key in (127, curses.KEY_BACKSPACE):
                    if self.cursor_position == 24:
                        pass
                    
                    elif self.cursor_position - 24 == len(filename):
                        filename = filename[:-1]
                        self.stdscr.move(self.height - 2, 24)
                        self.stdscr.clrtoeol()
                        self.stdscr.refresh()
                        for i in range(len(filename)):
                            self.stdscr.addstr(self.height - 2, 24 + i, filename[i], curses.color_pair(1))
                        self.cursor_position = 24 + len(filename)

                    else:
                        filename = filename[:self.cursor_position - 25] + filename[self.cursor_position - 24:]

                        self.stdscr.move(self.height - 2, 24)
                        self.stdscr.clrtoeol()
                        self.stdscr.refresh()

                        for i in range(len(filename)):
                            self.stdscr.addstr(self.height - 2, 24 + i, filename[i], curses.color_pair(1))
                        self.cursor_position -= 1
                        self.stdscr.move(self.height - 2, self.cursor_position)

                elif key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
                    if key == curses.KEY_UP or key == curses.KEY_DOWN:
                        pass

                    elif key == curses.KEY_LEFT and self.cursor_position == 24:
                        pass

                    elif key == curses.KEY_RIGHT and self.cursor_position == 24 + len(filename):
                        pass

                    else:
                        if key == curses.KEY_LEFT:
                            self.cursor_position -= 1
                            self.stdscr.move(self.height - 2, self.cursor_position)

                        elif key == curses.KEY_RIGHT:
                            self.cursor_position += 1
                            self.stdscr.move(self.height - 2, self.cursor_position)

                else:
                    self.stdscr.move(self.height - 2, 24)
                    self.stdscr.clrtoeol()
                    
                    filename = filename[:self.cursor_position - 24] + chr(key) + filename[self.cursor_position - 24:]
                    self.stdscr.refresh()
                    
                    for i in range(len(filename)):
                        self.stdscr.addstr(self.height - 2, 24 + i, filename[i], curses.color_pair(1))
                    self.cursor_position = 24 + len(filename)
                    self.stdscr.move(self.height - 2, self.cursor_position)

            
            self.stdscr.addstr(self.height - 2, 0, "File has been saved!", curses.color_pair(1))
            self.stdscr.refresh()
            time.sleep(1.5)
            self.stdscr.move(self.height - 2, 0)
            self.stdscr.clrtoeol()
            self.redraw_text()
            self.stdscr.refresh()
            self.cursor_position = 0

        except Exception:
            self.stdscr.addstr(self.height - 2, 0, "File has not been saved!", curses.color_pair(1))
            self.stdscr.refresh()
            time.sleep(1.5)
            self.stdscr.move(self.height - 2, 0)
            self.stdscr.clrtoeol()
            self.redraw_text()
            self.stdscr.refresh()
            self.cursor_position = 0


    def open_file(self):
        pass


