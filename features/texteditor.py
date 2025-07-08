class TextEditor:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.text = []
        self.current_line = 0
        self.cursor_position = 0

    def run(self, Flag=False):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:
            self.display_text()
            key = self.stdscr.getch()
            self.handle_input(key, Flag)

            if Flag == True:
                break # Exit the editor
        
        self.save_file()

    def display_text(self):

        for i, line in enumerate(self.text):
            self.stdscr.addstr(i, 0, line)


    def handle_input(self, key, Flag):
        
        if key == 27: # Escape key
            Flag = True # Set a flag to exit

    
    def save_file(self):
        pass
