class TextEditor:

    def __init__(self, filename):
        self.filename = filename
        self.text = ""

    def write(self, content):
        """Write content to the file."""
        with open(self.filename, "w") as file:
            file.write(content)