from sympy import Symbol, Pow

a = Symbol('a')
b = Symbol('b')

# Input values from the user
base = int(input("Enter the base (a): "))
exponent = int(input("Enter the exponent (b): "))

# Build the tetration expression
result = a ** a

for _ in range(2, exponent):
    result = a ** result

# Calculate the tetration
result = result.subs({a: base})

# Display the result
print(f"{base} tetrated to the power {exponent} is equal to {result}")
