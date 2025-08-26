#  Day 3: Arrays & Objects

from functools import reduce

# Arrays (Lists) in Python
numbers = [10, 20, 30, 40, 50]

# map -> using list comprehension
doubled = [num * 2 for num in numbers]

# filter -> using list comprehension
filtered = [num for num in numbers if num > 25]

# reduce -> sum
sum_numbers = reduce(lambda acc, num: acc + num, numbers, 0)

print("Original Numbers:", numbers)
print("Doubled:", doubled)
print("Filtered (>25):", filtered)
print("Sum:", sum_numbers)


# Objects & Nested Objects -> Dictionaries
student = {
    "name": "Aman",
    "age": 21,
    "marks": {
        "math": 85,
        "science": 90,
        "english": 78
    }
}

print("\nStudent Name:", student["name"])
print("Math Marks:", student["marks"]["math"])


# List of Dictionaries (Similar to array of objects)
students = [
    {"name": "Aman", "marks": [85, 90, 78]},
    {"name": "Riya", "marks": [88, 76, 95]},
    {"name": "Karan", "marks": [70, 65, 80]}
]

def calculate_average(marks):
    return sum(marks) / len(marks)

for s in students:
    avg = calculate_average(s["marks"])
    print(f"\nStudent: {s['name']}")
    print("Marks:", s["marks"])
    print("Average:", round(avg, 2))
