from rich.console import Console  # For colored output
from rich.text import Text          # For styled text
import pyfiglet                    # For ASCII art
import time
import os
import curses
from features.menu import console  # Import console from menu.py which is the main function of that script

console_instance = Console()  # Avoid conflict with the imported function

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def fig_entrance(text):
    """Display entrance text in slanted ASCII art."""
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    console_instance.print(ascii_art)

def colorized_message(message, color="cyan"):
    """Print a colorized message."""
    if color == "white":
        text = Text(message, style=color)
        console_instance.print(text)
    else:
        for i in message:
            i = Text(i, style=color)
            console_instance.print(i, end="")
            time.sleep(0.05)

def main():
    """Main function."""
    try:
        fig_entrance("Pronto!")  # Entrance art
        time.sleep(0.35)
        colorized_message("Welcome to My Project!\n", "bold magenta")
        time.sleep(0.25)
        colorized_message("Press Enter to continue...", "yellow")
        input()  # Wait for user input
        clear()
        fig_entrance("Pronto!")
        colorized_message("     ---------------------------      ", "white")
        
        # Call the console function from menu.py
        curses.wrapper(console)  # This line runs the console function in a curses context
                                 # For stdscr usage

    except ModuleNotFoundError:
        colorized_message("\nModule not found", "red")
        colorized_message("\nInstall requirements from requirements.txt", "red")
    except EOFError:
        colorized_message("\nAn unexpected error occurred", "red")
    except KeyboardInterrupt:
        colorized_message("\nAn unexpected error occurred", "red")

if __name__ == "__main__":
    main()