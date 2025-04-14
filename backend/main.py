from flask import Flask, request, jsonify
from Classes.Graph import Graph
from Classes.SignalGraphSolver import SignalGraphSolver
import traceback

from mssgDTOs.InputDTO import InputDTO

app = Flask(__name__)

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
        result = solver.solve()
        
        return jsonify({
            "success": True,
            "result": result
        }), 200
    
    except Exception as e:
        traceback.print_exc() 
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True)