from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- import CORS
from Classes.Graph import Graph
from Classes.SignalGraphSolver import SignalGraphSolver
from Stability.Routh_criteria import routh_criteria
import traceback
from mssgDTOs.InputDTO import InputDTO
import numpy as np

app = Flask(__name__)
CORS(app)  # <--- allow all origins (for development)

@app.route('/graph', methods=['POST'])
def create_graph():
    try:
        data = request.json.get("edges", [])
        dto = InputDTO(data)
        graph = Graph(dto)
        return jsonify(graph.graph)
    except Exception as e:
        traceback.print_exc() 
        return jsonify({"error": str(e)}), 400

@app.route('/solve', methods=['POST'])
def solve_signal_flow_graph():
    try:
        data = request.json.get("edges", [])
        dto = InputDTO(data)
        graph = Graph(dto)
        start_nodes = graph.get_start_nodes()
        end_nodes = graph.get_end_nodes()
        if len(start_nodes) != 1 or len(end_nodes) != 1:
            raise ValueError("Graph must have exactly one start node and one end node.")

        paths = graph.get_all_paths(start_nodes[0], end_nodes[0])
        solver = SignalGraphSolver(graph.get_all_loops(), paths)
        result, delta, deltas, gains, loop_pairs, forward_paths = solver.solve()
        loop_pairs = [[[loop.nodes for loop in sublist] for sublist in level] for level in loop_pairs]
        forward_paths_gains = [path.gain for path in forward_paths]
        forward_paths_nodes = [path.path for path in forward_paths]
        return jsonify({
            "success": True,
            "result": result,
            "delta": delta,
            "deltas": deltas,
            "Forward_paths_gains": forward_paths_gains,
            "Forward_paths_nodes": forward_paths_nodes,
            "loop_pairs_gains": gains,
            "loop_pairs": loop_pairs
        }), 200

    except Exception as e:
        traceback.print_exc() 
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    
@app.route("/solve_characteristic_equation", methods=["POST"])
def solve_characteristic_equation():
    try:
        
        data = request.get_json()
        coeffs = data['coeffs']
        order = data['order']
        result = routh_criteria(coeffs, order)
        
        def convert_complex(obj):
            if isinstance(obj, (complex, np.complex128, np.complex64)):
                return {"real": obj.real, "imag": obj.imag}
            elif isinstance(obj, np.ndarray):  # Convert NumPy arrays to lists
                return obj.tolist()
            elif isinstance(obj, list):  # Recursively process lists
                return [convert_complex(item) for item in obj]
            elif isinstance(obj, dict):  # Recursively process dictionaries
                return {key: convert_complex(value) for key, value in obj.items()}
            else:
                return obj 
        
        result = convert_complex(result)
        return jsonify(result)
    
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run()
