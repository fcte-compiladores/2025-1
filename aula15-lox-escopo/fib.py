def fib(n):
    if n <= 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

n = float(input("n: "))

for i in range(int(n)):
    print(fib(i + 0.0))