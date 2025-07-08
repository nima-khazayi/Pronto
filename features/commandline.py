import subprocess

class CommandLineInterface:

    def __init__(self):
        self.history = []

    def execute_command(self, command):
        """Execute a shell command."""
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            return str(e)