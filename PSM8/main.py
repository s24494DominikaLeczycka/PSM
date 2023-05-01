import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


def count_neighbors(grid):
    kernel = np.array([[1, 1, 1],
                       [1, 0, 1],
                       [1, 1, 1]])

    return convolve2d(grid, kernel, mode='same', boundary='wrap')


def game_of_life(grid, rules):
    survive, birth = rules

    # Count neighbors for all cells
    neighbors = count_neighbors(grid)

    # Apply game rules using NumPy boolean indexing
    old_grid = grid.copy()
    new_grid = grid.copy()
    new_grid[(grid == 1) & ~np.isin(neighbors, survive)] = 0
    new_grid[(grid == 0) & np.isin(neighbors, birth)] = 1

    # Generate color information
    colors = np.zeros_like(new_grid, dtype=int)
    colors[(old_grid == 1) & (new_grid == 0) & (neighbors < 2)] = 1  # Pink
    colors[(old_grid == 0) & (new_grid == 1)] = 2  # Blue
    colors[(old_grid == 1) & (new_grid == 1) & np.isin(neighbors, survive)] = 3  # Green
    colors[(old_grid == 1) & (new_grid == 0) & (neighbors > 3)] = 4  # Orange

    return new_grid, old_grid, colors
def on_key(event, canvas):
    if event.key == 'ctrl+c':
        plt.close()

def update(frame, grid, img_bw, img_colored, rules):
    grid[:], old_grid, colors = game_of_life(grid, rules)
    img_bw.set_array(grid)
    img_colored.set_array(colors)
    return img_bw, img_colored,

def main():
    grid_size = 50
    steps = 100
    survive = [2, 3]
    birth = [3]
    rules = (survive, birth)

    grid = np.random.choice([0, 1], grid_size * grid_size, p=[0.8, 0.2]).reshape(grid_size, grid_size)

    fig, (ax_bw, ax_colored) = plt.subplots(1, 2, figsize=(20, 7))

    img_bw = ax_bw.imshow(grid, cmap='binary', interpolation="nearest", vmin=0, vmax=1)
    _, _, colors = game_of_life(grid, rules)

    custom_cmap = ListedColormap(['white', 'pink', 'deepskyblue', 'limegreen', 'orange'])
    img_colored = ax_colored.imshow(colors, cmap=custom_cmap, interpolation="nearest", vmin=0, vmax=4)

    ani = animation.FuncAnimation(fig, update, fargs=(grid, img_bw, img_colored, rules), frames=steps, interval=200, blit=True)

    # Create legends
    legend_elements_bw = [Patch(facecolor='black', label='Living cells'),
                          Patch(facecolor='white', label='Dead cells')]
    ax_bw.legend(handles=legend_elements_bw, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)

    legend_elements_colored = [Patch(facecolor='pink', label='Dying out of loneliness'),
                                Patch(facecolor='deepskyblue', label='Newly born'),
                                Patch(facecolor='limegreen', label='Ideal neighbors'),
                                Patch(facecolor='orange', label='Dying due to overcrowding')]
    ax_colored.legend(handles=legend_elements_colored, loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0)

    # Add title
    fig.suptitle('The game of life', fontsize=16)

    # Bind keypress event to the on_key function
    canvas = fig.canvas
    canvas.mpl_connect('key_press_event', lambda event: on_key(event, canvas))

    plt.show()

if __name__ == "__main__":
    main()