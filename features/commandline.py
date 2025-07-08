import subprocess

class CommandLineInterface:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.history = []
        self.text = []
        self.current_line = 0
        self.cursor_position = 0


    def runner(self):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:
            self.display_text()
            key = self.stdscr.getch()
            self.handle_input(key)

            if key == 27: # Escape key
                break # Exit the editor
        
        self.save_file()

    def display_text(self):

        self.stdscr.clear()

        for i, line in enumerate(self.text):
            self.stdscr.addstr(i, 0, line)

        self.stdscr.move(self.current_line, self.cursor_position)
        self.stdscr.refresh()


    def handle_input(self, key):
        
        pass

    def save_file(self):
        pass

    def execute_command(self, command):
        """Execute a shell command."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)