import time
from .texteditor import TextEditor  # Use relative import
from .commandline import CommandLineInterface  # Use relative import

def console(stdscr):
    # Clear the screen
    stdscr.clear()
    
    hints = [
        "Hint: Ctrl+S to save.",
        "Hint: Ctrl+T to open the text editor.",
        "Hint: Ctrl+C to open the command line.",
        "Hint: Ctrl+X to go back from editor/command line.",
        "Hint: Press 'q' to quit."
    ]

    height, width = stdscr.getmaxyx()

    text_editor = None
    command_line = None

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Your main program goes here...")
        hint = hints[int(time.time()) % len(hints)]  # Cycle through hints
        stdscr.addstr(height - 2, 0, "Use any key to check the supported commands from hints!")
        stdscr.addstr(height - 1, 0, hint)

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == 19:  # Ctrl+S
            save_file()
        elif key == 20:  # Ctrl+T
            text_editor = TextEditor("your_file.txt")
            run_text_editor(stdscr, text_editor)
        elif key == 11:  # Ctrl+K
            command_line = CommandLineInterface()
            run_command_line(stdscr, command_line)
        elif key == 24:  # Ctrl+X
            if text_editor or command_line:
                # Go back to the menu
                text_editor = None
                command_line = None

def save_file():
    
    print("File saved!")  # Placeholder for actual saving logic

def run_text_editor(stdscr, text_editor):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Text Editor (Press Ctrl+X to go back)\n")
        stdscr.refresh()
        
        # Placeholder for actual texteditor functionality
        key = stdscr.getch()
        if key == 24:  # Ctrl+X
            break

def run_command_line(stdscr, command_line):
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Command Line Interface (Press Ctrl+X to go back)\n")
        stdscr.refresh()
        
        # Placeholder for actual commandline functionality
        key = stdscr.getch()
        if key == 24:  # Ctrl+X
            break