from flask import Flask, request, jsonify
from flask_cors import CORS
from mssgDTOs.inputDTO import inputDTO
from Stability.Routh_criteria import routh_criteria
from Graph import Graph
import numpy as np

app = Flask(__name__)
CORS(app)
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
    

if __name__ == "__main__":
    app.run(debug=True)
