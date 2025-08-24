// Day 3: Arrays & Objects
// Concepts: map, filter, reduce, objects, nested objects

// Array Methods

const numbers = [10, 20, 30, 40, 50];

const doubled = numbers.map(num => num * 2);

const filtered = numbers.filter(num => num > 25);

const sum = numbers.reduce((acc, num) => acc + num, 0);

console.log("Original Numbers:", numbers);
console.log("Doubled:", doubled);
console.log("Filtered (>25):", filtered);
console.log("Sum:", sum);


// Objects & Nested Objects

const student = {
  name: "Aman",
  age: 21,
  marks: {
    math: 85,
    science: 90,
    english: 78
  }
};

console.log("\nStudent Name:", student.name);
console.log("Math Marks:", student.marks.math);



const students = [
  { name: "Aman", marks: [85, 90, 78] },
  { name: "Riya", marks: [88, 76, 95] },
  { name: "Karan", marks: [70, 65, 80] }
];

function calculateAverage(marks) {
  return marks.reduce((acc, m) => acc + m, 0) / marks.length;
}

students.forEach(student => {
  const avg = calculateAverage(student.marks);
  console.log(`\nStudent: ${student.name}`);
  console.log("Marks:", student.marks);
  console.log("Average:", avg.toFixed(2));
});