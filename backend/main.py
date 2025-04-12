from Classes.Graph import Graph
# from Classes.SignalGraphSolver import SignalGraphSolver
from Classes.Loop import Loop

inputDTO = [
    {"from": "A", "to": "B", "gain": 2.0},
    {"from": "B", "to": "C", "gain": 3.0},
    {"from": "C", "to": "A", "gain": 4.0},  # Loop A -> B -> C -> A
    {"from": "C", "to": "D", "gain": 5.0},
    {"from": "D", "to": "B", "gain": 1.0}   # Another loop B -> C -> D -> B
]

g = Graph(inputDTO)
loops = g.get_all_loops()
for loop in loops:
    print(loop)
