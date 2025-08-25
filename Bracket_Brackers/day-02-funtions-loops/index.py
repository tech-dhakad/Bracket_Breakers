#  Day 2: Functions & Loops
#  Task: Find highest marks from an array
def find_highest(marks):
    highest = marks[0]

    for mark in marks:
        if mark > highest:
            highest= mark
    return highest

marks =[67,89,56,78,99,85]

print("Marks:",marks)
print("Highest Marks",find_highest(marks))


            
