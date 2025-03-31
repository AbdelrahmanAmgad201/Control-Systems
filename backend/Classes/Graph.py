class Graph:
    graph: dict[str, dict[str, float]]

    def __init__(self, inputDTO):
        self.graph = self.construct(inputDTO)

    def construct(self, inputDTO):
        """
        Constructs graph from input data
        Expected format: list of edges [{"from": node1, "to": node2, "gain": value}, ...]
        """
        graph = {}
        
        for edge in inputDTO:
            from_node = edge["from"]
            to_node = edge["to"]
            gain = float(edge["gain"])
            
            if from_node not in graph:
                graph[from_node] = {}
            
            graph[from_node][to_node] = gain
            
            # Make sure to_node exists in graph even if it has no outgoing edges
            if to_node not in graph:
                graph[to_node] = {}
                
        return graph

    def get_start_node(self):
        all_nodes = set(self.graph.keys())
        nodes_with_incoming_edges = set()
        
        # Find all nodes that have incoming edges
        for source, targets in self.graph.items():
            for target in targets.keys():
                nodes_with_incoming_edges.add(target)
        
        # Find nodes without incoming edges
        start_nodes = all_nodes - nodes_with_incoming_edges
        
        if len(start_nodes) != 1:
            raise ValueError(f"Expected exactly one start node, but found: {len(start_nodes)} {start_nodes}")
        
        return next(iter(start_nodes))

    def get_end_node(self):
        end_nodes = [node for node, neighbors in self.graph.items() if not neighbors]
        
        if len(end_nodes) != 1:
            raise ValueError(f"Expected exactly one end node, but found: {len(end_nodes)} {end_nodes}")
        
        return end_nodes[0]