def fib(n):
    if (n <= 1):
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

n = int(input("n: "))

for i in range(n):
    print(fib(i + 0.0))

