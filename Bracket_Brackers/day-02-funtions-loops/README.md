# 📘 Day 2: Functions & Loops – Mini Task

##  Task
Find the *highest marks* from an array using *functions, conditionals, and loops* in Python.

---

## 🛠 Concepts Covered
- *Functions* → Reusable code blocks  
- *Conditionals* → if statement to compare values  
- *Loops* → Iterating over arrays (for, while)  

---

##  Solution (Using Function + For Loop)

```python
# Function to find the highest marks
def find_highest(marks):
    # Assume first element is the highest initially
    highest = marks[0]
    
    # Loop through the list
    for mark in marks:
        if mark > highest:
            highest = mark
    return highest


# Example usage
marks = [67, 89, 56, 92, 78, 99, 85]

print("Marks:", marks)
print("Highest Marks:", find_highest(marks))