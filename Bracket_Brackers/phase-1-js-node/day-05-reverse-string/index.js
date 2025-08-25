// Day 5: Express.js Basics

const express = require("express");
const app = express();

app.use(express.json());


app.get("/", (req, res) => {
  res.send("Welcome to Express.js 🚀");
});

app.post("/greet", (req, res) => {
  const { name } = req.body;
  res.send(`Hello, ${name}! Nice to meet you `);
});

app.get("/students", (req, res) => {
  const students = [
    { id: 1, name: "Aarav", age: 20 },
    { id: 2, name: "Ishita", age: 21 },
    { id: 3, name: "Rohan", age: 19 }
  ];
  res.json(students);
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`✅ Express server running at http://localhost:${PORT}`);
});