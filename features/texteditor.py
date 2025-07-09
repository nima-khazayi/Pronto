import curses
import time

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = []
        self.current_line = 0
        self.cursor_position = 0
        self.blinking = True

    def run(self):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:
            
            self.positioning()
            key = self.stdscr.getch()
            if self.handle_input(key):
                break # Exit the editor
            
            self.display_text()
            
            self.cursor_blink()
        
        self.save_file()

    def display_text(self):

        for i, line in enumerate(self.text):
            self.stdscr.addstr(0, i, line)


    def handle_input(self, key):

        height, width = self.stdscr.getmaxyx()
        
        if key == 27: # Escape key
            return True # Set a flag to exit
        
        elif key == 127 or key == curses.KEY_BACKSPACE:
            pass

        elif key == 10 or key == curses.KEY_ENTER:
            self.current_line += 1

        else:
            self.text.append(chr(key))


    
    def save_file(self):
        pass


    def cursor_blink(self):
        self.blinking = not self.blinking


    def positioning(self):

        height, width = self.stdscr.getmaxyx()
        position = f"Row: {self.current_line},   Col: {self.cursor_position}"
        self.stdscr.addstr(height - 1, width // 2 - 15, position, curses.A_BOLD)




