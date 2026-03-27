def isPrime(num):
    if (num <= 1): return False
    if (num == 2): return True
    if (num % 2 == 0): return False

    i = 3
    while i * i <= num:
        if (num % i == 0): return False
        i += 2
    return True

count = 0
number = 2

prime = int(input("Input the prime number: "))
while count < prime:
    if isPrime(number): count += 1
    if (count == prime): break
    number += 1
print(f"Prime number {prime}: {number}")