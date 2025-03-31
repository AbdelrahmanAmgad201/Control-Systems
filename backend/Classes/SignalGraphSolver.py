from dataclasses import dataclass
from typing import List, Set, Tuple, Dict

class SignalGraphSolver:
    @dataclass
    class Path:
        gain: float
        path: List[str]
        
        def __str__(self):
            return f"Path {' -> '.join(self.path)} with gain {self.gain}"

    @dataclass
    class Loop:
        gain: float
        nodes: List[str]
        
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

    @staticmethod
    def Controller(graph):
        # Called in Main
        try:
            # Validate the graph first
            try:
                start_node = graph.get_start_node()
                end_node = graph.get_end_node()
            except ValueError as e:
                print(f"Error: {e}")
                return {
                    "error": str(e),
                    "solved": False
                }
                
            # Graph is valid, proceed with solving
            return SignalGraphSolver._solve(graph)
        except Exception as e:
            print(f"Error solving signal flow graph: {e}")
            return {
                "error": str(e),
                "solved": False
            }

    @staticmethod
    def _solve(graph):
        # At this point, we know the graph has exactly one start and one end node
        start_node = graph.get_start_node()
        end_node = graph.get_end_node()
        
        # Step 1: Find all forward paths
        forward_paths = SignalGraphSolver.find_all_paths(graph, start_node, end_node)
        
        if not forward_paths:
            error_msg = f"No forward paths found from start node {start_node} to end node {end_node}"
            print(f"Error: {error_msg}")
            return {
                "error": error_msg,
                "solved": False
            }
        
        # Step 2: Find all loops
        loops = SignalGraphSolver.find_all_loops(graph)
        
        # Step 3: Calculate delta (determinant)
        delta = SignalGraphSolver.calculate_delta(loops)
        
        # Step 4: Calculate delta_i for each forward path
        deltas_i = []
        for path in forward_paths:
            touching_loops = [loop for loop in loops if any(node in path.path for node in loop.nodes)]
            delta_i = SignalGraphSolver.calculate_delta(loops, touching_loops)
            deltas_i.append(delta_i)
        
        # Step 5: Apply Mason's formula
        if abs(delta) < 1e-10:  # Near zero
            error_msg = "Graph determinant is zero, transfer function is undefined"
            print(f"Error: {error_msg}")
            return {
                "error": error_msg,
                "solved": False
            }
        
        transfer_function = sum(path.gain * delta_i for path, delta_i in zip(forward_paths, deltas_i)) / delta
        
        result = {
            "transfer_function": transfer_function,
            "forward_paths": forward_paths,
            "loops": loops,
            "delta": delta,
            "deltas_i": deltas_i,
            "solved": True
        }
        
        return result

    @staticmethod
    def find_all_paths(graph, start, end, visited=None, path=None, gain=None):
        """Find all possible paths from start to end"""
        if visited is None:
            visited = set()
            path = []
            gain = 1.0
            result = []
        else:
            result = []
        
        visited.add(start)
        path.append(start)
        
        if start == end:
            result.append(SignalGraphSolver.Path(gain=gain, path=path.copy()))
        else:
            for neighbor, edge_gain in graph.graph.get(start, {}).items():
                if neighbor not in visited:
                    new_gain = gain * edge_gain
                    result.extend(SignalGraphSolver.find_all_paths(
                        graph, neighbor, end, visited.copy(), path.copy(), new_gain
                    ))
        
        return result

    @staticmethod
    def find_all_loops(graph):
        """Find all loops in the graph"""
        loops = []
        
        for start_node in graph.graph:
            loops.extend(SignalGraphSolver._find_loops_from_node(graph, start_node))
        
        # Remove duplicate loops (same nodes in different order)
        unique_loops = []
        loop_node_sets = set()
        
        for loop in loops:
            # Sort loop nodes to create a canonical representation
            sorted_nodes = sorted(loop.nodes)
            node_tuple = tuple(sorted_nodes)
            
            if node_tuple not in loop_node_sets and len(node_tuple) > 0:
                loop_node_sets.add(node_tuple)
                unique_loops.append(loop)
        
        return unique_loops

    @staticmethod
    def _find_loops_from_node(graph, start_node, current_node=None, visited=None, path=None, gain=None):
        """Find all loops starting from a specific node"""
        if current_node is None:
            current_node = start_node
            visited = set()
            path = []
            gain = 1.0
            result = []
        else:
            result = []
        
        visited.add(current_node)
        path.append(current_node)
        
        for neighbor, edge_gain in graph.graph.get(current_node, {}).items():
            if neighbor == start_node and len(path) > 1:
                # Found a loop
                loop_gain = gain * edge_gain
                result.append(SignalGraphSolver.Loop(gain=loop_gain, nodes=path.copy()))
            elif neighbor not in visited:
                new_gain = gain * edge_gain
                result.extend(SignalGraphSolver._find_loops_from_node(
                    graph, start_node, neighbor, visited.copy(), path.copy(), new_gain
                ))
        
        return result

    @staticmethod
    def calculate_delta(all_loops, touching_loops=None):
        """
        Calculate the determinant using loops and non-touching loops
        Delta = 1 - sum(all loop gains) + sum(products of gains of two non-touching loops) - ...
        
        If touching_loops is provided, exclude these loops and any loops that touch them
        """
        if not all_loops:
            return 1.0  # No loops means delta is 1
            
        if touching_loops is None:
            loops_to_exclude = set()
        else:
            # Exclude loops that touch any loop in touching_loops
            loops_to_exclude = set(id(loop) for loop in touching_loops)
                
        # Filter out excluded loops
        loops = [loop for loop in all_loops if id(loop) not in loops_to_exclude]
        
        if not loops:
            return 1.0  # All loops are excluded
            
        # Start with 1
        delta = 1.0
        
        # Subtract sum of all loop gains
        delta -= sum(loop.gain for loop in loops)
        
        # For small graphs, we might not need to check non-touching loops
        if len(loops) <= 1:
            return delta
            
        # Add sum of products of two non-touching loops
        pairs = SignalGraphSolver._get_non_touching_groups(loops, 2)
        if pairs:
            delta += sum(SignalGraphSolver._product_of_gains(pair) for pair in pairs)
        
        # Subtract sum of products of three non-touching loops
        if len(loops) >= 3:
            triplets = SignalGraphSolver._get_non_touching_groups(loops, 3)
            if triplets:
                delta -= sum(SignalGraphSolver._product_of_gains(triplet) for triplet in triplets)
        
        # Add sum of products of four non-touching loops
        if len(loops) >= 4:
            quads = SignalGraphSolver._get_non_touching_groups(loops, 4)
            if quads:
                delta += sum(SignalGraphSolver._product_of_gains(quad) for quad in quads)
        
        return delta

    @staticmethod
    def _get_non_touching_groups(loops, k):
        """Find all groups of k non-touching loops"""
        if not loops or k <= 0 or k > len(loops):
            return []
        return SignalGraphSolver._find_non_touching_groups(loops, [], 0, k)

    @staticmethod
    def _find_non_touching_groups(loops, current_group, start_idx, k):
        """Recursive helper to find non-touching groups"""
        if k == 0:
            return [current_group]
        
        if start_idx >= len(loops):
            return []
            
        result = []
        for i in range(start_idx, len(loops)):
            loop = loops[i]
            
            # Check if this loop touches any in the current group
            if not any(loop.touches(other) for other in current_group):
                result.extend(
                    SignalGraphSolver._find_non_touching_groups(
                        loops, current_group + [loop], i + 1, k - 1
                    )
                )
        
        return result

    @staticmethod
    def _product_of_gains(loops):
        """Calculate product of gains for a group of loops"""
        product = 1.0
        for loop in loops:
            product *= loop.gain
        return product