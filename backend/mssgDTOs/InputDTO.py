from typing import List, Dict

class InputDTO:
    def __init__(self, data: List[List]):
        self.edges = [{"from": edge[0], "to": edge[1], "gain": edge[2]} for edge in data]