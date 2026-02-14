def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Can't divide by zero")
    return a / b


if __name__ == "__main__":
    print("Calc Demo")
    print("6 + 7 =", add(6, 7))
    print("6 - 7 =", subtract(6, 7))
    print("6 * 7 =", multiply(6, 7))
    print("10 / 5 =", divide(10, 5))