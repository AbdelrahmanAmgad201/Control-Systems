from Classes.Graph import Graph
from mssgDTOs.InputDTO import InputDTO

data = [["A", "B", 1.5], ["B", "C", 2.0], ["A", "C", 3.0]]
dto = InputDTO(data)
g = Graph(dto)
print(g.graph)
