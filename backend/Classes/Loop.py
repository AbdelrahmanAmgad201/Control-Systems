from dataclasses import dataclass
from typing import List, Set, Tuple, Dict

class Loop:
        gain: float
        nodes: List[str]
        def __init__(self):
            pass
        def __str__(self):
            nodes_str = ' -> '.join(self.nodes)
            if self.nodes:
                nodes_str += f" -> {self.nodes[0]}"
            return f"Loop {nodes_str} with gain {self.gain}"
        
        def touches(self, path_or_loop) -> bool:
            """Check if this loop shares any nodes with path or another loop"""
            loop_nodes = set(self.nodes)
            other_nodes = set(path_or_loop.path if hasattr(path_or_loop, 'path') else path_or_loop.nodes)
            return len(loop_nodes.intersection(other_nodes)) > 0