"""Plotting of grids / tasks

originally from: https://www.kaggle.com/boliu0/visualizing-all-task-pairs-with-gridlines
"""

import matplotlib
import matplotlib.pyplot as plt


color_map = matplotlib.colors.ListedColormap(
    [
        "#000000",
        "#0074D9",
        "#FF4136",
        "#2ECC40",
        "#FFDC00",
        "#AAAAAA",
        "#F012BE",
        "#FF851B",
        "#7FDBFF",
        "#870C25",
    ]
)

color_normalization = colors.Normalize(vmin=0, vmax=9)


def plot_grid(grid, ax, title=None):
    input_matrix = task[train_or_test][i][input_or_output]
    ax.imshow(grid, cmap=color_map, norm=color_normalization)
    ax.grid(True, which="both", color="lightgrey", linewidth=0.5)
    ax.set_yticks([x - 0.5 for x in range(1 + len(grid))])
    ax.set_xticks([x - 0.5 for x in range(1 + len(grid[0]))])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_title(title)
