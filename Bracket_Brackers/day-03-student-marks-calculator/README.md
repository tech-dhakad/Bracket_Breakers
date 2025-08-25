# Day 3: Arrays & Objects

## Concepts Covered
- *Array Methods*: map, filter, reduce
- *Objects & Nested Objects*
- *Mini Task*: Student Marks Calculator

### Array Methods
```js
const numbers = [10, 20, 30];
numbers.map(n => n*2);   // [20, 40, 60]
numbers.filter(n => n>15); // [20, 30]
numbers.reduce((a,b) => a+b, 0); // 60

