from flask import Flask, request, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "Rahul", "age": 20},
    {"id": 2, "name": "Priya", "age": 22}
]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Student CRUD API"}), 200

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students), 200

@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Invalid data"}), 400
    new_id = max([s["id"] for s in students], default=0) + 1
    new_student = {"id": new_id, "name": data["name"], "age": data["age"]}
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    data = request.get_json()
    student["name"] = data.get("name", student["name"])
    student["age"] = data.get("age", student["age"])
    return jsonify(student), 200

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Student deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
