from flask import Flask, request, jsonify

from game_engine import FlaskController

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        json_request = request.get_json()
        return jsonify({"response": FlaskController.analyse_request(json_request)}), 200
    else:
        return jsonify({"About": "A Checkers game in unity against an AI."})


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
