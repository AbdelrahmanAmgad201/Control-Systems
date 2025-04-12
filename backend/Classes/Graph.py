from typing import List, Dict, Set
from .Loop import Loop
from .Path import Path
import copy

class Graph:
    graph: Dict[str, Dict[str, float]]

    def __init__(self, inputDTO):
        self.graph = self.construct(inputDTO)

    def construct(self, inputDTO):
        graph = {}
        for edge in inputDTO:
            frm = edge["from"]
            to = edge["to"]
            gain = edge["gain"]

            if frm not in graph:
                graph[frm] = {}
            graph[frm][to] = gain
            if to not in graph:
                graph[to] = {}
        return graph

    def get_start_nodes(self):
        all_from_nodes = set(self.graph.keys())
        all_to_nodes = {to for neighbors in self.graph.values() for to in neighbors}
        return list(all_from_nodes - all_to_nodes)

    def get_end_nodes(self):
        return [node for node, neighbors in self.graph.items() if not neighbors]

    def get_all_loops(self) -> List[Loop]:
        visited_loops = []
        all_loops_set = set()  # Store canonical loop signatures

        def canonical_form(nodes: List[str]) -> tuple:
            """Rotate list so the smallest element is first"""
            n = len(nodes)
            min_index = min(range(n), key=lambda i: nodes[i])
            return tuple(nodes[min_index:] + nodes[:min_index])

        def dfs(current, start, path, gain, visited_set):
            neighbors = self.graph.get(current, {})
            for neighbor, weight in neighbors.items():
                if neighbor == start:
                    loop_nodes = path[:]  # full loop without duplicating start
                    canonical = canonical_form(loop_nodes)
                    if canonical not in all_loops_set:
                        all_loops_set.add(canonical)
                        total_gain = gain * weight
                        loop = Loop()
                        loop.nodes = copy.deepcopy(loop_nodes)
                        loop.gain = total_gain
                        visited_loops.append(loop)
                elif neighbor not in visited_set:
                    visited_set.add(neighbor)
                    dfs(neighbor, start, path + [neighbor], gain * weight, visited_set)
                    visited_set.remove(neighbor)

        for node in self.graph:
            dfs(node, node, [node], 1.0, {node})

        return visited_loops
    def get_all_paths(self, start: str, end: str) -> List[Path]:
        all_paths = []

        def dfs(current, path, gain, visited):
            if current == end:
                all_paths.append(Path(path, gain))
                return
            for neighbor, weight in self.graph.get(current, {}).items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    dfs(neighbor, path + [neighbor], gain * weight, visited)
                    visited.remove(neighbor)

        dfs(start, [start], 1.0, {start})
        return all_paths

