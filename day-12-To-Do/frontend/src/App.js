import React, { useEffect, useState } from "react";

function App() {
  const [todos, setTodos] = useState([]);
  const [task, setTask] = useState("");

 
  const fetchTodos = async () => {
    const response = await fetch("http://127.0.0.1:5000/todos");
    const data = await response.json();
    setTodos(data);
  };

  useEffect(() => {
    fetchTodos();
  }, []);


  const addTodo = async () => {
    if (!task) return;
    const response = await fetch("http://127.0.0.1:5000/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task })
    });
    const newTodo = await response.json();
    setTodos([...todos, newTodo]);
    setTask("");
  };


  const deleteTodo = async (id) => {
    await fetch(`http://127.0.0.1:5000/todos/${id}`, { method: "DELETE" });
    setTodos(todos.filter((todo) => todo.id !== id));
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>To-Do App</h1>
      <input
        type="text"
        placeholder="Add new task"
        value={task}
        onChange={(e) => setTask(e.target.value)}
      />
      <button onClick={addTodo}>Add</button>

      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            {todo.task}{" "}
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
