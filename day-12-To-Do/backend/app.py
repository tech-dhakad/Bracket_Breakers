from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

todos = [
    {"id": 1, "task": "Learn React"},
    {"id": 2, "task": "Practice Python"}
]

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if "task" not in data:
        return jsonify({"error": "Task is required"}), 400
    new_id = max([todo["id"] for todo in todos], default=0) + 1
    new_todo = {"id": new_id, "task": data["task"]}
    todos.append(new_todo)
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
