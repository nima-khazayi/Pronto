import curses
import pyfiglet
import time

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 8
        self.cursor_position = 0
        self.length = [0]
        self.height, self.width = self.stdscr.getmaxyx()

    def run(self):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:

            message = pyfiglet.figlet_format("TextEditor", font="slant")
            self.stdscr.addstr(0, 1, message)
            self.stdscr.addstr(6, 2, "     ---------------------------      ")
            self.movement()
            key = self.stdscr.getch()
            if self.handle_input(key):
                break # Exit the editor

            self.stdscr.refresh()

    def display_text(self):

        for char in (self.text):
            self.stdscr.addstr(self.current_line, self.cursor_position, char)


    def handle_input(self, key):
        
        if key == 27: # Escape key
            return True # Set a flag to exit
        
        elif key == 127 or key == curses.KEY_BACKSPACE:
            if self.cursor_position != 0:
                self.stdscr.addstr(self.current_line, self.cursor_position, " ")
                self.text = self.text[:-1]
                self.positioning(key)
                self.stdscr.refresh()

            else:
                self.positioning(key)
                self.stdscr.refresh()

        else:
            self.positioning(key)

    def positioning(self, key=None):
        
        if key in (10, curses.KEY_ENTER):
            self.enter()
        
        elif key in (127, curses.KEY_BACKSPACE):
            self.remove()

        elif key == 6:
            self.save_file()

        elif key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            self.arrows(key)
            
        else:
            if self.cursor_position + 2 == self.width:
                self.enter()

            self.text += chr(key)
            self.cursor_position += 1
            self.display_text()
            self.length.append(self.cursor_position)
            self.length.pop(-2)
            
        # Clear previous position display
        self.stdscr.move(self.height - 1, 0)
        self.stdscr.clrtoeol()
        
        # Draw new position
        position = f"Row: {self.current_line - 7}, Col: {self.cursor_position + 1}"
        self.stdscr.addstr(self.height - 1, self.width // 2 - len(position) // 2, position, curses.A_BOLD)
        self.stdscr.refresh()

        self.movement()

        
    def movement(self):
        self.stdscr.move(self.current_line, self.cursor_position + 1)


    def arrows(self, key):
        if key == curses.KEY_UP:
            if self.current_line > 8:
                self.current_line -= 1
                prev_line_len = self.length[self.current_line - 8]
                self.cursor_position = min(self.cursor_position, prev_line_len)
                self.movement()

        elif key == curses.KEY_DOWN:
            if self.current_line - 8 < len(self.length) - 1:
                self.current_line += 1
                next_line_len = self.length[self.current_line - 8]
                self.cursor_position = min(self.cursor_position, next_line_len)
                self.movement()

        elif key == curses.KEY_LEFT:
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.movement()
            elif self.current_line > 8:
                self.current_line -= 1
                self.cursor_position = self.length[self.current_line - 8]
                self.movement()

        elif key == curses.KEY_RIGHT:
            line_len = self.length[self.current_line - 8]
            if self.cursor_position < line_len:
                self.cursor_position += 1
                self.movement()
            elif self.current_line - 8 < len(self.length) - 1:
                self.current_line += 1
                self.cursor_position = 0
                self.movement()

        

    def remove(self):
        if self.cursor_position == 0 and self.current_line == 8:
            self.length.pop()
            self.length.append(0)
        
        elif self.cursor_position == 0:
            self.current_line -= 1
            self.cursor_position = self.length[-2]
            self.length.pop()
            self.movement()
            
        else:
            self.cursor_position -= 1
            self.movement()
            self.length.append(self.length[-1] - 1)
            self.length.pop(-2)

    def enter(self):
        self.text += "\n"
        self.length.append(0)
        self.current_line += 1
        self.cursor_position = 0


    def save_file(self):
        file = open("file.txt", "w")
        file.write(self.text)

        # Initialize color support
        curses.start_color()
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # Display the green message
        self.stdscr.addstr(self.height - 2, 0, "File has been saved!", curses.color_pair(1))

        # Refresh the screen to show the changes
        self.stdscr.refresh()
        time.sleep(1.5)
        self.stdscr.move(self.height - 2, 0)
        self.stdscr.clrtoeol()
        self.stdscr.refresh()

