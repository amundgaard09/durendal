import numpy as np
import matplotlib.pyplot as plt
from numba import cuda

@cuda.jit
def mandelbrot_kernel(output: np.ndarray, x_min, x_max, y_min, y_max, max_iter: int):
    col, row = cuda.grid(2)
    
    height, width = output.shape

    if col < width and row < height:
        c_real = x_min + col * (x_max - x_min) / width
        c_imag = y_min + row * (y_max - y_min) / height
        
        z_real = 0.0
        z_imag = 0.0
        
        iteration = max_iter
        for i in range(max_iter):
            new_z_real = z_real**2 - z_imag**2 + c_real
            new_z_imag = 2.0 * z_real * z_imag + c_imag
            
            z_real = new_z_real
            z_imag = new_z_imag
            
            if (z_real**2 + z_imag**2) > 4.0:
                iteration = i
                break
        
        output[row, col] = iteration

width, height = 1000, 1000
x_range, y_range = (-2.0, 0.5), (-1.25, 1.25)
max_iter = 256

mandelbrot_data = np.empty((height, width), dtype=np.int32)

d_mandelbrot_data = cuda.to_device(mandelbrot_data)

threadsperblock = (16, 16)
blockspergrid_x = int(np.ceil(width / threadsperblock[0]))
blockspergrid_y = int(np.ceil(height / threadsperblock[1]))
blockspergrid = (blockspergrid_x, blockspergrid_y)

mandelbrot_kernel[blockspergrid, threadsperblock](
    d_mandelbrot_data, x_range[0], x_range[1], y_range[0], y_range[1], max_iter
)

result = d_mandelbrot_data.copy_to_host()

plt.figure(figsize=(10, 8))
plt.imshow(result, extent=[*x_range, *y_range], cmap='magma')
plt.colorbar(label='Iterations to Escape')
plt.show()