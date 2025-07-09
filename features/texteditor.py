import curses

class TextEditor:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 0
        self.cursor_position = 0

    def run(self):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:
            
            self.stdscr.refresh()

            key = self.stdscr.getch()
            if self.handle_input(key):
                break # Exit the editor

            self.display_text()
        
        self.save_file()

    def display_text(self):

        for char in (self.text):
            self.stdscr.addstr(self.current_line, self.cursor_position, char)


    def handle_input(self, key):
        
        if key == 27: # Escape key
            return True # Set a flag to exit
        
        elif key == 127 or key == curses.KEY_BACKSPACE:
            self.positioning(key)

        elif key == 10 or key == curses.KEY_ENTER:
            self.positioning(key)

        else:
            self.positioning(key)

    
    def save_file(self):
        pass

    def positioning(self, key=None):

        height, width = self.stdscr.getmaxyx()
        position = f"Row: {self.current_line + 1},   Col: {self.cursor_position + 1}"
        self.stdscr.addstr(height - 1, width // 2 - 15, position, curses.A_BOLD)

        if key in (10, curses.KEY_ENTER):
            self.cursor_position = 0
            self.current_line += 1
        
        elif key in (127, curses.KEY_BACKSPACE):
            if self.cursor_position > 0:
                self.cursor_position -= 1
                self.text.replace(self.text[-1], "")
                
                # Clear the last character from the screen
                self.stdscr.addstr(self.current_line, self.cursor_position, ' ')
                
                # Check if we are at the start of a line
                if self.cursor_position == 0 and self.current_line > 0:
                    self.current_line -= 1
                    self.cursor_position = len(self.text)  # Move cursor to the end of the previous line

        else:

            self.text += chr(key)
        
            if self.cursor_position >= width:
                self.cursor_position = 0
                self.current_line += 1

            else:
                self.cursor_position += 1


        self.stdscr.move(self.current_line, self.cursor_position)




