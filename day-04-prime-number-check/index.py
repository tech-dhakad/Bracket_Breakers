from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    PORT = 4000
    app.run(host="0.0.0.0", port=PORT, debug=True)
