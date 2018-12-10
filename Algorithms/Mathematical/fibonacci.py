def fibo(number):
    if number == 0:
        return number
    if number == 1:
        return number
    return fibo(number-1) + fibo(number-2)

if __name__ == '__main__':
    series = []
    for i in range(10):
        series.append(fibo(i))
    print(", ".join(map(str,series)))
