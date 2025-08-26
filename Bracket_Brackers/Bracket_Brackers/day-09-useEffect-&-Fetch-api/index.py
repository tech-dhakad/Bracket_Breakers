from flask import Flask, jsonify, render_template

app = Flask(__name__)

students = [
    {"id": 1, "name": "Aarav", "age": 20},
    {"id": 2, "name": "Ishita", "age": 21},
    {"id": 3, "name": "Rohan", "age": 19}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students")
def get_students():
    return jsonify(students)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
