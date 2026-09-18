
fib = int(input("Enter the index number of the Fibonacci number: "))

list = [0, 1]

for i in range (2, fib):
    list.append(list[0] + list[1])
    list.pop(0)
print(f"Answer: {list[1]}")