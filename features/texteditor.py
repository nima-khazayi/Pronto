import curses
import pyfiglet

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 8
        self.cursor_position = 0
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
        
        self.save_file()

    def display_text(self):

        for char in (self.text):
            self.stdscr.addstr(self.current_line, self.cursor_position, char)


    def handle_input(self, key):
        
        if key == 27: # Escape key
            return True # Set a flag to exit
        
        elif key == 127 or key == curses.KEY_BACKSPACE:
            self.positioning(key)
            self.display_text()

        elif key == 10 or key == curses.KEY_ENTER:
            self.positioning(key)

        else:
            self.positioning(key)

    
    def save_file(self):
        pass

    def positioning(self, key=None):
        
        if key in (10, curses.KEY_ENTER):
            self.current_line += 1
            self.cursor_position = 0
        
        elif key in (127, curses.KEY_BACKSPACE):
            pass

        else:
            self.cursor_position += 1
            self.text += chr(key)
            self.display_text()
            
        # Clear previous position display
        self.stdscr.move(self.height - 1, 0)
        self.stdscr.clrtoeol()
        
        # Draw new position
        position = f"Row: {self.current_line + 1}, Col: {self.cursor_position + 1}"
        self.stdscr.addstr(self.height - 1, self.width // 2 - len(position) // 2, position, curses.A_BOLD)
        self.stdscr.refresh()

        self.movement()

        
    def movement(self):
        if self.cursor_position + 2 == self.width:
            self.positioning(curses.KEY_ENTER)

        self.stdscr.move(self.current_line, self.cursor_position + 1)

        


