
fib = int(input("Введите порядковый номер числа фиббоначи: "))

list = [0, 1]

for i in range (2, fib):
    list.append(list[0] + list[1])
    list.pop(0)
print(f"Ответ: {list[1]}")