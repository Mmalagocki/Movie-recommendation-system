import random

file_name = "task.csv"

file = open(file_name, "r")

for line in file:
    print(line.rstrip().replace("NULL", str(random.randint(0, 5))))