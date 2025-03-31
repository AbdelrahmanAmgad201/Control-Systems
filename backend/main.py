from Classes.Graph import Graph
from Classes.SignalGraphSolver import SignalGraphSolver

def main():
    # Example 1: Valid graph with one start and one end node
    print("Example 1: Valid graph")
    edges1 = [
        {"from": "A", "to": "B", "gain": 2.0},
        {"from": "B", "to": "C", "gain": 3.0},
        {"from": "C", "to": "D", "gain": 1.0}
    ]
    
    graph1 = Graph(edges1)
    result1 = SignalGraphSolver.Controller(graph1)
    
    if result1.get("solved", False):
        print(f"Transfer Function: {result1['transfer_function']}")
        print("\nForward Paths:")
        for path in result1['forward_paths']:
            print(f"  {path}")
        print("\nLoops:")
        for loop in result1['loops']:
            print(f"  {loop}")
        print(f"\nDelta: {result1['delta']}")
    else:
        print(f"Could not solve: {result1.get('error', 'Unknown error')}")
    
    
    # Example 2: Invalid graph with multiple start nodes
    print("\n\nExample 2: Invalid graph - multiple start nodes")
    edges2 = [
        {"from": "A", "to": "C", "gain": 2.0},
        {"from": "B", "to": "C", "gain": 3.0},
        {"from": "C", "to": "D", "gain": 1.0}
    ]
    
    graph2 = Graph(edges2)
    result2 = SignalGraphSolver.Controller(graph2)
    
    if result2.get("solved", False):
        print(f"Transfer Function: {result2['transfer_function']}")
    else:
        print(f"Could not solve: {result2.get('error', 'Unknown error')}")
    
    
    # Example 3: Invalid graph with no start node (cycle)
    print("\n\nExample 3: Invalid graph - no start node (cycle)")
    edges3 = [
        {"from": "A", "to": "B", "gain": 2.0},
        {"from": "B", "to": "C", "gain": 3.0},
        {"from": "C", "to": "A", "gain": 1.0}
    ]
    
    graph3 = Graph(edges3)
    result3 = SignalGraphSolver.Controller(graph3)
    
    if result3.get("solved", False):
        print(f"Transfer Function: {result3['transfer_function']}")
    else:
        print(f"Could not solve: {result3.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()