from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Welcome to Flask 🚀"

@app.route("/greet", methods=["POST"])
def greet():
    data = request.get_json()
    name = data.get("name", "Guest")
    return f"Hello, {name}! Nice to meet you"

@app.route("/students", methods=["GET"])
def get_students():
    students = [
        {"id": 1, "name": "Aarav", "age": 20},
        {"id": 2, "name": "Ishita", "age": 21},
        {"id": 3, "name": "Rohan", "age": 19}
    ]
    return jsonify(students)

if __name__ == "__main__":
    PORT = 3000
    app.run(host="0.0.0.0", port=PORT, debug=True)
