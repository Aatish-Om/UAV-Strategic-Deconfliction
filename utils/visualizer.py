# utils/visualizer.py

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_uavs(primary_path, other_paths, conflicts):
    primary = np.array(primary_path)
    others_np = {k: np.array(v) for k, v in other_paths.items()}

    root = tk.Tk()
    root.title("UAV Deconfliction System")

    fig = plt.Figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title("3D UAV Path with Conflicts")
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 60)
    ax.set_zlim(0, 60)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()

    # Line + point for primary
    primary_line, = ax.plot([], [], [], 'b-', label='Primary')
    primary_point, = ax.plot([], [], [], 'bo')

    # Lines + points for others
    other_lines = {}
    other_points = {}
    colors = ['r', 'g', 'm']
    for i, (name, path) in enumerate(others_np.items()):
        other_lines[name], = ax.plot([], [], [], linestyle='--', color=colors[i % len(colors)], label=name)
        other_points[name], = ax.plot([], [], [], marker='o', color=colors[i % len(colors)])

    conflict_scatters = []

    def update(frame):
        if frame < len(primary):
            primary_line.set_data(primary[:frame+1, 0], primary[:frame+1, 1])
            primary_line.set_3d_properties(primary[:frame+1, 2])
            primary_point.set_data(primary[frame, 0], primary[frame, 1])
            primary_point.set_3d_properties(primary[frame, 2])

        for name, path in others_np.items():
            if frame < len(path):
                other_lines[name].set_data(path[:frame+1, 0], path[:frame+1, 1])
                other_lines[name].set_3d_properties(path[:frame+1, 2])
                other_points[name].set_data(path[frame, 0], path[frame, 1])
                other_points[name].set_3d_properties(path[frame, 2])

        for (x, y, z, t, name) in conflicts:
            if t == frame:
                scatter = ax.scatter(x, y, z, c='red', marker='x', s=100)
                ax.text(x, y, z, f"{name}@t={t}", color='red')
                conflict_scatters.append(scatter)

        return [primary_line, primary_point] + list(other_lines.values()) + list(other_points.values()) + conflict_scatters

    ani = FuncAnimation(fig, update, frames=range(len(primary)), interval=1000, repeat=False)
    canvas.draw()

    # Add Start button if needed
    tk.Button(root, text="Exit", command=root.destroy).pack()
    root.mainloop()

