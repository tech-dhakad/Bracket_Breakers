# Day 4: Python API with Flask

This project demonstrates how to create a **basic API in Python** similar to a **Node.js Express app**.

---

## Concepts Covered
- Setting up a **Flask** web server
- Creating a **GET endpoint**
- Returning **JSON responses**

---

## Code Overview
- `@app.route("/")` → Handles **GET requests** at the root URL (`/`)
- `jsonify()` → Converts Python dictionaries to **JSON response**
- Runs on `http://localhost:4000`

---

## Sample Output
When you visit `http://localhost:4000` in your browser or use **Postman**:

```json
{
  "message": "Hello, World!"
}
