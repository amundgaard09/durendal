
def f(x: float) -> float:
    return 2.5 * x ** 2 - 3.1 * x + 4.7

points = []

print("\n")

for i in range(6):
    print(f"f({i}) = {f(i):.2f}")
    points.append(f(i))
    
print(f"Bunnpunktet er på x: {points.index(min(points))} y: {min(points)}")

print("\n")