from rich.console import Console  # For colored output
from rich.text import Text          # For styled text
import pyfiglet                    # For ASCII art

console = Console()

def fig_entrance(text):
    """Display entrance text in slanted ASCII art."""
    ascii_art = pyfiglet.figlet_format(text, font="slant")
    console.print(ascii_art)

def colorized_message(message, color="cyan"):
    """Print a colorized message."""
    text = Text(message, style=color)
    console.print(text)

def main():
    """Main function."""
    try:
        fig_entrance("Pronto!")  # Entrance art
        colorized_message("Welcome to My Project!", "bold magenta")
        colorized_message("Press Enter to continue...", "green")
        input()  # Wait for user input
        
    except ModuleNotFoundError as e:
        colorized_message("Module not found: " + str(e), "red")
        colorized_message("Install requirements from requirements.txt", "red")
    except Exception as e:
        colorized_message("An unexpected error occurred: " + str(e), "red")

if __name__ == "__main__":
    main()