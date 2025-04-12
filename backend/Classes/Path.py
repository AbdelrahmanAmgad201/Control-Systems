from typing import List

class Path:
    def __init__(self, path: List[str], gain: float):
        self.path = path
        self.gain = gain

    def __str__(self):
        return f"Path {' -> '.join(self.path)} with gain {self.gain}"
