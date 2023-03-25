import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def count_neighbors(grid, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                count += grid[(x + i) % grid.shape[0], (y + j) % grid.shape[1]]
    return count

def game_of_life(grid, rules):
    survive, birth = rules
    new_grid = grid.copy()
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            neighbors = count_neighbors(grid, x, y)
            if grid[x, y] and neighbors not in survive:
                new_grid[x, y] = 0
            elif not grid[x, y] and neighbors in birth:
                new_grid[x, y] = 1
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