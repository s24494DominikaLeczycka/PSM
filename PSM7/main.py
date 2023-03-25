import numpy as np
import matplotlib.pyplot as plt

def laplace_solver(n, edge_temps):
    # Initialize the grid
    grid = np.zeros((n, n))

    # Set edge temperatures
    grid[0, :] = edge_temps["top"]
    grid[-1, :] = edge_temps["bottom"]
    grid[:, 0] = edge_temps["left"]
    grid[:, -1] = edge_temps["right"]

    # Compute the coefficient matrix A and the known terms vector b
    N = (n - 2) ** 2
    A = np.zeros((N, N))
    b = np.zeros(N)

    row = 0
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            A[row, row] = 4

            if j > 1:
                A[row, row - 1] = -1
            else:
                b[row] -= edge_temps["left"]

            if j < n - 2:
                A[row, row + 1] = -1
            else:
                b[row] -= edge_temps["right"]

            if i > 1:
                A[row, row - (n - 2)] = -1
            else:
                b[row] -= edge_temps["top"]

            if i < n - 2:
                A[row, row + (n - 2)] = -1
            else:
                b[row] -= edge_temps["bottom"]

            row += 1

    # Solve the system of linear equations Ax = b
    x = np.linalg.solve(A, b)

    # Update the grid with the calculated temperatures
    grid[1:-1, 1:-1] = x.reshape((n - 2, n - 2))

    return grid

def plot_temperature_distribution(grid):
    plt.imshow(grid, cmap='hot', origin='upper')
    plt.colorbar(label='Temperature')
    plt.title('Temperature Distribution Inside the Plate')
    plt.show()

if __name__ == "__main__":
    n = 41
    edge_temps = {
        "top": 75,
        "bottom": 50,
        "left": 100,
        "right": 0
    }

    grid = laplace_solver(n, edge_temps)
    plot_temperature_distribution(grid)
