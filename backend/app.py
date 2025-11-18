from flask import Flask, request, jsonify
from flask_cors import CORS
from model import get_response

app = Flask(__name__)
CORS(app)

@app.route("/query", methods=["POST"])
def ask_query():
    data = request.get_json()

    if not data or "query" not in data:
        return jsonify({"error": "query missing"}), 400

    answer = get_response(data["query"])
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
