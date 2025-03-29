from flask import Flask, request, jsonify
from mssgDTOs.inputDTO import inputDTO
from Stability.Routh_criteria import routh_criteria
from Graph import Graph
import numpy as np

app = Flask(__name__)

@app.route("/process_graph", methods=["POST"])
def process_graph():
    pass

@app.route("/solve_characteristic_equation", methods=["POST"])
def solve_characteristic_equation():
    try:
        
        data = request.get_json()
        coeffs = data['coeffs']
        order = data['order']
        result = routh_criteria(coeffs, order)
        if 'matrix' in result and isinstance(result['matrix'], np.ndarray):
            result['matrix'] = result['matrix'].tolist()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == "__main__":
    app.run(debug=True)
