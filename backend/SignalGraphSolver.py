from .Graph import Graph  # Correct import

class SignalGraphSolver:

    @staticmethod
    def Controller(Graph):
        # Called in Main
        return SignalGraphSolver._solve(Graph)

    @staticmethod
    def _solve(Graph):
        # All solving Logic
        start_node = Graph.get_start_node()
        end_node = Graph.get_end_node()
        pass
