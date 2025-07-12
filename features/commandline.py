import subprocess
import curses
import pyfiglet
import select

class CommandLineInterface:

    def __init__(self):
        self.stdscr = curses.initscr()
        self.text = ""
        self.current_line = 8
        self.cursor_position = 0
        self.history = []
        self.length = [0]
        self.height, self.width = self.stdscr.getmaxyx()


    def run(self):
        """Run a cell in terminal for displaying the editor"""
        self.stdscr.clear()
        self.stdscr.refresh()

        while True:

            message = pyfiglet.figlet_format("CommandLine", font="slant")
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
            self.stdscr.clear()
            return True # Set a flag to exit
        

        else:
            self.positioning(key)
        

    def positioning(self, key):

        if key in (10, curses.KEY_ENTER):
            self.execute_command(self.text)

        else:
            self.text += chr(key)
            self.cursor_position += 1
            self.display_text()
            self.length.append(self.cursor_position)
            self.length.pop(-2)

        self.movement()

    def movement(self):
        self.stdscr.move(self.current_line, self.cursor_position + 1)

    def execute_command(self, command):
        """Execute a shell command."""
        try:
            self.stdscr.clear()

            # Start subprocess
            proc = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    text=True,
                                    bufsize=1)

            line_num = 0
            while proc.poll() is None:
                ready, _, _ = select.select([proc.stdout], [], [], 0.1)
                if ready:
                    line = proc.stdout.readline()
                    if line:
                        self.stdscr.addstr(line_num, 0, line.strip())
                        line_num += 1
                        self.stdscr.refresh()

            # Read remaining lines after process ends
            for line in proc.stdout:
                self.stdscr.addstr(line_num, 0, line.strip())
                line_num += 1
                self.stdscr.refresh()

            self.history.append(command)
            self.text = ""
            self.current_line = 8
            self.cursor_position = 0
            key = self.stdscr.getch()
            self.handle_input(key)

        except Exception as e:
            return str(e)