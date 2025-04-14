from dataclasses import dataclass
from typing import List, Set, Tuple, Dict
from Graph import Graph
from Loop import Loop
import itertools

class SignalGraphSolver:
    def __init__(self, G: List[Loop]):
        self.all_loops = G
        self.all_pairof_loops = []  # Each element is a list of combinations of loops of a certain order
        self.gains = []

        self.all_pairof_loops.append([[loop] for loop in self.all_loops])
        self.gains.append([loop.gain for loop in self.all_loops])
    
    def get_non_touching_loops(self):
        max_order = len(self.all_loops)
        for order in range(2, max_order + 1):
            current_combinations = []
            current_gains = []
            if order == 2:
                for combo in itertools.combinations(self.all_loops, order):
                    if self.are_mutually_non_touching(combo):
                        current_combinations.append(list(combo))
                        current_gains.append(self.combo_gain(combo))
            else:
                prev_order_index = order - 2 
                for prev_combo in self.all_pairof_loops[prev_order_index]:
                    for loop in self.all_loops:
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
                self.gains.append(current_gains)
            else:
                break
                
        return self.gains, self.all_pairof_loops
    
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

test_loops = []
test_loops.append(loop1)
test_loops.append(loop2)
test_loops.append(loop3)
test_loops.append(loop4)
test_loops.append(loop5)

solver = SignalGraphSolver(test_loops)
gains, loops = solver.get_non_touching_loops()
print("Gains:", gains)
print("\nNon-touching loop combinations:")
for order, combinations in enumerate(loops, 1):
    print(f"\nOrder {order}:")
    for combo_index, combo in enumerate(combinations):
        nodes_list = [loop.nodes for loop in combo]
        print(f"  Combination {combo_index+1}: {nodes_list}, Gain: {gains[order-1][combo_index]}")