class Graph:
    graph: dict[str, dict[str, int]]

    def __init__(self, inputDTO):
        self.graph = self.construct(inputDTO)

    def construct(self, inputDTO):
        pass 

    def get_start_node(self):
        all_nodes = set(self.graph.keys())
        nodes_with_incoming_edges = {target for neighbors in self.graph.values() for target in neighbors}

        start_nodes = all_nodes - nodes_with_incoming_edges

        if len(start_nodes) != 1:
            raise ValueError(f"Expected exactly one start node, but found: {start_nodes}")
        
        return next(iter(start_nodes))

    def get_end_node(self):
        end_nodes = [node for node, neighbors in self.graph.items() if not neighbors]

        if len(end_nodes) != 1:
            raise ValueError(f"Expected exactly one end node, but found: {end_nodes}")
        
        return end_nodes[0]
