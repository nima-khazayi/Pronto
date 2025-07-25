import curses
from .texteditor import TextEditor  # Use relative import
from .commandline import CommandLineInterface  # Use relative import

def console(stdscr):
    # Clear the screen
    stdscr.clear()
    
    hints = [
        "Hint: Ctrl+F to save.",
        "Hint: Ctrl+T to open the text editor.",
        "Hint: Ctrl+K to open the command line.",
        "Hint: Esc to go back from editor/command line.",
        "Hint: Press 'q' to quit."
    ]

    height, width = stdscr.getmaxyx()

    text_editor = None
    command_line = None
    i = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Your main program goes here...")
        hint = hints[i % len(hints)]  # Cycle through hints
        i += 1
        stdscr.addstr(height - 2, 0, "Use any key to check the supported commands from hints!", curses.A_BOLD)
        stdscr.addstr(height - 1, 0, hint)

        stdscr.refresh()
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == 20:  # Ctrl+T
            text_editor = TextEditor()
            text_editor.run()
        elif key == 11:  # Ctrl+K
            command_line = CommandLineInterface()
            command_line.run()