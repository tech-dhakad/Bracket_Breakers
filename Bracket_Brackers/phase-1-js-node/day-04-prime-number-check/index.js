// Day 4: Node.js intro
// Task: API with Express
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.json({ message: "Hello, World!" });
});

const PORT = 4000;
app.listen(PORT, () => {
  console.log(`API running at http://localhost:${PORT}`);
});