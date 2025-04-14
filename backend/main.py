from Classes.Graph import Graph
from Classes.SignalGraphSolver import SignalGraphSolver
from Classes.Loop import Loop

from flask import Flask, request, jsonify
from typing import Dict
import json

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_signal_flow_graph():
    try:
        
        input_data = request.json
        graph = Graph(input_data)
        solver = SignalGraphSolver(graph)
        result = solver.solve()
        
        return jsonify({
            "success": True,
            "result": result
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == '__main__':
    app.run(debug=True)