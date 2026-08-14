# graph_plotter.py
#
# Why this file exists:
# The assignment asks us to draw a graph showing the original
# points, the interpolation curve, and the estimated point. All
# the matplotlib code for this is kept here so it does not mix
# with the math code in interpolation.py.

from pathlib import Path

import numpy as np
import matplotlib
# "Agg" backend lets matplotlib save images without needing a
# screen/display, which is important because this program might
# run on a server or a computer without a GUI.
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Number of points used to draw the smooth curve line.
# More points = smoother curve, but slower to calculate.
CURVE_RESOLUTION = 300

# If the dataset has more original points than this, drawing every
# single one on the graph (and using every single one to build the
# curve) becomes too slow and the graph becomes unreadable anyway.
# So above this limit, we only use a smaller sample of the data
# just for the picture. The actual math answer (in the output
# file) still uses the FULL dataset, this limit is only for the
# graph image.
MAX_POINTS_FOR_GRAPH = 200


class GraphPlotter:
    """
    Responsible only for drawing and saving graphs.
    Does not do any interpolation math itself, it just receives
    already-calculated values and plots them.
    """

    def _get_sample_for_plotting(self, x_values, y_values):
        # Picks a smaller sample of points to plot when the
        # dataset is too big, so the graph stays readable and
        # fast to draw.
        if len(x_values) <= MAX_POINTS_FOR_GRAPH:
            return x_values, y_values

        step = len(x_values) // MAX_POINTS_FOR_GRAPH
        sample_x = x_values[::step]
        sample_y = y_values[::step]
        return sample_x, sample_y

    def plot_and_save(self, interpolation_object, point, estimated_value,
                       question_name, save_path):
        # interpolation_object -> the LagrangeInterpolation object
        #                          (already has x and y stored in it)
        # point                -> the x value we estimated
        # estimated_value      -> the f(point) result we calculated
        # question_name        -> just used for the graph title
        # save_path            -> where to save the .png file

        x_values = interpolation_object.x
        y_values = interpolation_object.y

        # Building the smooth curve line.
        # We draw the curve a little bit before the smallest x and
        # a little bit after the biggest x, so the picture looks
        # nicer and not cut off at the edges.
        x_min = min(x_values)
        x_max = max(x_values)
        padding = (x_max - x_min) * 0.1 if x_max != x_min else 1

        curve_x = np.linspace(x_min - padding, x_max + padding, CURVE_RESOLUTION)
        curve_y = interpolation_object.estimate_many(curve_x)

        # Getting a smaller sample of original points if the
        # dataset is huge, just for drawing purposes.
        plot_x, plot_y = self._get_sample_for_plotting(x_values, y_values)

        # Now we actually draw the graph.
        plt.figure(figsize=(8, 6))

        plt.plot(curve_x, curve_y, color="blue", label="Interpolation Curve")
        plt.scatter(plot_x, plot_y, color="red", label="Given Data Points", zorder=5)
        plt.scatter([point], [estimated_value], color="green", marker="*",
                    s=200, label="Estimated Point", zorder=6)

        plt.title(f"Lagrange Interpolation - {question_name}")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid(True)

        # Making sure the "graphs" folder actually exists before
        # we try to save the picture into it.
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)

        # Saving in high resolution as asked in the requirements.
        plt.savefig(save_path, dpi=300)
        plt.close()

        print(f"Graph saved to: {save_path}")

        return curve_x, curve_y
