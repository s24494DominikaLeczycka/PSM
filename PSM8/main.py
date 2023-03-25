import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def count_neighbors(grid):
    # Using np.roll to shift the grid in all 8 directions and then summing them up
    up = np.roll(grid, -1, axis=0)
    down = np.roll(grid, 1, axis=0)
    left = np.roll(grid, -1, axis=1)
    right = np.roll(grid, 1, axis=1)

    up_left = np.roll(up, -1, axis=1)
    up_right = np.roll(up, 1, axis=1)
    down_left = np.roll(down, -1, axis=1)
    down_right = np.roll(down, 1, axis=1)

    return up + down + left + right + up_left + up_right + down_left + down_right

def game_of_life(grid, rules):
    survive, birth = rules

    # Count neighbors for all cells
    neighbors = count_neighbors(grid)

    # Apply game rules using NumPy boolean indexing
    new_grid = grid.copy()
    new_grid[(grid == 1) & ~np.isin(neighbors, survive)] = 0
    new_grid[(grid == 0) & np.isin(neighbors, birth)] = 1

    return new_grid

def update(frame, grid, img, rules):
    grid[:] = game_of_life(grid, rules)
    img.set_array(grid)
    return img,

def main():
    grid_size = 50
    steps = 100
    survive = [2, 3]
    birth = [3]
    rules = (survive, birth)

    grid = np.random.choice([0, 1], grid_size * grid_size, p=[0.8, 0.2]).reshape(grid_size, grid_size)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, cmap="binary", interpolation="nearest")
    ani = animation.FuncAnimation(fig, update, fargs=(grid, img, rules), frames=steps, interval=200, blit=True)
    plt.show()

if __name__ == "__main__":
    main()
