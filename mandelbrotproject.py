
def mandelbrotcheck(c: complex, Iterations):
    """
    Check if the given complex number `c` diverges or stays bounded through the Mandelbrot function:
    
    `z_n+1` = `(z_n)^2` + `c`.
    """
    
    z = 0
    
    for n in range(Iterations):
        if abs(z) > 2:
            return n
        z = z**2 + c
    return Iterations

def colorize(val):    
    color = 16 + (val % 200)
    return f"\033[38;5;{color}m██"

width = 150
height = 150

matrix = [[0 for _ in range(width)] for _ in range(height)]

for x in range(width):
    for y in range(height):
        real = -2 + (x / height) * 3 
        imag = -1.5 + (y / width) * 3

        c = complex(real, imag)
        iterations = mandelbrotcheck(c, 1000)

        matrix[y][x] = iterations
        
for row in matrix:
    line = ""
    for val in row:
        line += colorize(val)
    line += "\033[0m"
    print(line)