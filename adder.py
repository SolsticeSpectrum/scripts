def add(a, b):
    while b != 0:
        carry = a and b
        a = a ^ b
        b = (carry and (not a)) << 1
    return a

# Test the adder
num1 = 5
num2 = 3
result = add(num1, num2)
print(f"{num1} plus {num2} equals {result}")
