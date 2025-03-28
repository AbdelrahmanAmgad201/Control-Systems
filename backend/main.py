from flask import Flask, request, jsonify
from mssgDTOs.inputDTO import inputDTO
from Graph import Graph

app = Flask(__name__)

@app.route("/process_graph", methods=["POST"])
def process_graph():
    pass

@app.route("/solve_characteristic_equation", methods=["POST"])
def solve_characteristic_equation():
    pass

if __name__ == "__main__":
    app.run(debug=True)
