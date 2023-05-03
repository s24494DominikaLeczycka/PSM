# This code is an interactive implementation of Conway's Game of Life in Python. The simulation displays two visualizations side-by-side: one showing the cells in black and white (alive or dead) and the other presenting cells with colors according to their state (dying due to loneliness, newly born, ideal neighbors, or dying due to overcrowding). Users can update the rules for cell survival and birth, restart the animation, and view the simulation in real-time.

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import convolve2d
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.widgets import Button
import tkinter as tk
from tkinter import simpledialog

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
def restart_animation(fig, grid, grid_size):
    grid[:] = np.random.choice([0, 1], grid_size * grid_size, p=[0.8, 0.2]).reshape(grid_size, grid_size)
    fig.canvas.draw_idle()

def change_rules(event, rules):
    def submit():
        survive_str = e_survive.get()
        birth_str = e_birth.get()
        survive = [int(x) for x in survive_str.split(",")]
        birth = [int(x) for x in birth_str.split(",")]
        rules[0] = survive
        rules[1] = birth
        input_dialog.destroy()

    input_dialog = tk.Tk()
    input_dialog.title("Update Rules")

    tk.Label(input_dialog, text="Survive rules (separated by a comma): ").grid(row=0, column=0)
    e_survive = tk.Entry(input_dialog)
    e_survive.grid(row=0, column=1)

    tk.Label(input_dialog, text="Birth rules (separated by a comma): ").grid(row=1, column=0)
    e_birth = tk.Entry(input_dialog)
    e_birth.grid(row=1, column=1)

    tk.Button(input_dialog, text="Submit", command=submit).grid(row=2, column=1)

    input_dialog.mainloop()

def on_key(event, fig, grid, grid_size, rules):
    if event.key == 'ctrl+c':
        plt.close()
    elif event.key == 'r':
        restart_animation(fig, grid, grid_size)
    elif event.key == 'u':
        change_rules(event, rules)

def update(frame, grid, img_bw, img_colored, rules):
    grid[:], old_grid, colors = game_of_life(grid, rules)
    img_bw.set_array(grid)
    img_colored.set_array(colors)
    return img_bw, img_colored,

def main():
    grid_size = 100
    steps = 100
    survive = [2, 3]
    birth = [3]
    rules = [survive, birth]  # Use a list instead of a tuple

    grid = np.random.choice([0, 1], grid_size * grid_size, p=[0.8, 0.2]).reshape(grid_size, grid_size)

    fig, (ax_bw, ax_colored) = plt.subplots(1, 2, figsize=(21, 7))

    img_bw = ax_bw.imshow(grid, cmap='binary', interpolation="nearest", vmin=0, vmax=1)
    _, _, colors = game_of_life(grid, rules)

    custom_cmap = ListedColormap(['white', 'pink', 'deepskyblue', 'limegreen', 'orange'])
    img_colored = ax_colored.imshow(colors, cmap=custom_cmap, interpolation="nearest", vmin=0, vmax=4)

    ani = animation.FuncAnimation(fig, update, fargs=(grid, img_bw, img_colored, rules), frames=steps, interval=0, blit=True)

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
    canvas.mpl_connect('key_press_event', lambda event: on_key(event, fig, grid, grid_size, rules))

    fig.subplots_adjust(bottom=0.2)  # Add space at the bottom for buttons

    # Add buttons for restarting the animation and updating the rules
    restart_button_ax = plt.axes([0.35, 0.05, 0.1, 0.075])
    restart_button = Button(restart_button_ax, 'Restart')
    restart_button.on_clicked(lambda event: restart_animation(event, grid, grid_size))

    update_rules_button_ax = plt.axes([0.55, 0.05, 0.1, 0.075])
    update_rules_button = Button(update_rules_button_ax, 'Update Rules')
    update_rules_button.on_clicked(lambda event: change_rules(event, rules))

    plt.show()

if __name__ == "__main__":
    main()