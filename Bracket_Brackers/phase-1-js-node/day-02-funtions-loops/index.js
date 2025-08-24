// Day 2: Functions & Loops
// Task: Find highest marks from an array


const marks = [78, 92, 85, 64, 99, 73, 88];


function findHighest(marksArray) {
  let highest = marksArray[0]; 
  for (let i = 1; i < marksArray.length; i++) {
    if (marksArray[i] > highest) {
      highest = marksArray[i];
    }
  }
  return highest;
}


const topScore = findHighest(marks);
console.log("Marks:", marks);
console.log("Highest Marks:", topScore);