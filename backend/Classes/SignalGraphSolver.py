from typing import List
from Classes.Loop import Loop
from Classes.Path import Path
from Classes.Graph import Graph
import itertools


class SignalGraphSolver:
    def __init__(self, loops: List[Loop], paths:List[Path]):
        self.all_loops = loops
        self.all_pairof_loops = []  # Each element is a list of combinations of loops of a certain order

        self.paths=paths  
        self.all_pairof_loops.append([[loop] for loop in self.all_loops])

        
    
    def get_non_touching_loops(self,all_loops):
        gains=[]
        gains.append([loop.gain for loop in all_loops])
        max_order = len(all_loops)
        for order in range(2, max_order + 1):
            current_combinations = []
            current_gains = []
            if order == 2:
                for combo in itertools.combinations(all_loops, order):
                    if self.are_mutually_non_touching(combo):
                        current_combinations.append(list(combo))
                        current_gains.append(self.combo_gain(combo))
            else:
                prev_order_index = order - 2 
                for prev_combo in self.all_pairof_loops[prev_order_index]:
                    for loop in all_loops:
                        if loop not in prev_combo:
                            new_combo = prev_combo.copy()
                            new_combo.append(loop)
                            if self.are_mutually_non_touching(new_combo):
                                new_combo.sort(key=lambda x: id(x))
                                if not any(set(c) == set(new_combo) for c in current_combinations):
                                    current_combinations.append(new_combo)
                                    current_gains.append(self.combo_gain(new_combo))
            
            if current_combinations:
                self.all_pairof_loops.append(current_combinations)
                gains.append(current_gains)
            else:
                break
                
        return gains.copy(), self.all_pairof_loops.copy
    
    def are_mutually_non_touching(self, loops: List[Loop]) -> bool:
        for i in range(len(loops)):
            for j in range(i + 1, len(loops)):
                if loops[i].touches(loops[j]):
                    return False
        return True
    
    def combo_gain(self, loops: List[Loop]) -> float:
        gain = 1.0
        for loop in loops:
            gain *= loop.gain
        return gain
    def get_deltas(self):
        deltas = []
        for path in self.paths:
            # Find loops that don't touch this path
            non_touching_loops = []
            for loop in self.all_loops:
                touches_path = False
                for node in loop.nodes:
                    if node in path.path:
                        touches_path = True
                        break
                if not touches_path:
                    non_touching_loops.append(loop)
            
            # Create a temporary solver with just these loops
            temp_solver = SignalGraphSolver(non_touching_loops, [])
            delta = temp_solver.get_delta()
            deltas.append(delta)
        
        return deltas
    



    def get_delta(self):
        gains,loops=self.get_non_touching_loops(self.all_loops)
        res=0
        sign=-1
        for i in gains:
            sign*=-1
            for j in i: 
                res+=sign*j 
        return 1-res
    
    def solve(self):
        res=0
        deltas=self.get_deltas()
        delta=self.get_delta()
        for i in range(len(self.paths)):
            res+=self.paths[i].gain*deltas[i]
        res/=delta 
        return res

# Test code
loop1 = Loop()
loop1.nodes = ['A', 'B', 'C']
loop1.gain = 2.5

loop2 = Loop()
loop2.nodes = ['D', 'E']
loop2.gain = 1.2

loop3 = Loop()
loop3.nodes = ['C', 'D']
loop3.gain = 0.8

loop4 = Loop()
loop4.nodes = ['F', 'G']
loop4.gain = 3.0

loop5 = Loop()
loop5.nodes = ['K', 'P']
loop5.gain = 3.7

path1=Path(['A','B','C','D'],7)
path2=Path(['P','A','T','R'],7)
test_loops = []
test_loops.append(loop1)
test_loops.append(loop2)
test_loops.append(loop3)
test_loops.append(loop4)
test_loops.append(loop5)
test_paths=[]
test_paths.append(path1)
test_paths.append(path2)
solver = SignalGraphSolver(test_loops,test_paths)

print(solver.solve())

