import json
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import os

CONFLICT_DISTANCE = 5

def load_mission(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def euclidean_distance_3d(p1, p2):
    return np.sqrt((p1['x'] - p2['x'])**2 + (p1['y'] - p2['y'])**2 + (p1['z'] - p2['z'])**2)

def detect_conflicts(primary, drones):
    conflicts = []
    for t, p_point in enumerate(primary):
        for drone_name, path in drones.items():
            if t < len(path):
                d_point = path[t]
                dist = euclidean_distance_3d(p_point, d_point)
                if dist < CONFLICT_DISTANCE:
                    conflicts.append((t, p_point, drone_name))
    return conflicts

def save_updated_paths_txt(drones, filename='/home/atom/uav_deconfliction/mission_data/updated_paths.txt'):
    with open(filename, 'w') as f:
        for name, path in drones.items():
            for t, point in enumerate(path):
                line = f"{name}, x={point['x']:.2f}, y={point['y']:.2f}, z={point['z']:.2f}, t={t}\n"
                f.write(line)
    print(f"[INFO] Updated paths saved to {filename}")

def animate_paths(primary, drones, conflicts):
    ani = None
    manual_frame = 0

    def update(frame):
        nonlocal manual_frame
        manual_frame = frame
        for txt in conflict_texts:
            txt.remove()
        conflict_texts.clear()

        if frame < len(primary):
            p_line.set_data(p_x[:frame+1], p_y[:frame+1])
            p_line.set_3d_properties(p_z[:frame+1])

        for name, path in drones.items():
            d_x = [p['x'] for p in path[:min(frame+1, len(path))]]
            d_y = [p['y'] for p in path[:min(frame+1, len(path))]]
            d_z = [p['z'] for p in path[:min(frame+1, len(path))]]

            drone_lines[name].set_data(d_x, d_y)
            drone_lines[name].set_3d_properties(d_z)

            if frame < len(path):
                drone_markers[name].set_data([path[frame]['x']], [path[frame]['y']])
                drone_markers[name].set_3d_properties([path[frame]['z']])
            else:
                drone_markers[name].set_data([], [])
                drone_markers[name].set_3d_properties([])

        visible_conflicts = [(t, pos, d) for (t, pos, d) in conflicts if t <= frame]
        if visible_conflicts:
            xs, ys, zs = zip(*[(p['x'], p['y'], p['z']) for (_, p, _) in visible_conflicts])
            red_dots._offsets3d = (xs, ys, zs)
            for t, p, d in visible_conflicts:
                label = f"({p['x']:.1f}, {p['y']:.1f}, {p['z']:.1f}) @ t={t}"
                txt = ax.text(p['x'], p['y'], p['z'], label, color='red', fontsize=8)
                conflict_texts.append(txt)
        else:
            red_dots._offsets3d = ([], [], [])

        time_text.set_text(f"Time Step: {frame}")
        canvas.draw()

    def start_animation():
        nonlocal ani
        if ani is None:
            ani = FuncAnimation(fig, update, frames=max_frames, interval=500, repeat=False)
            canvas.draw()

    def stop_program():
        root.destroy()

    def next_frame():
        nonlocal manual_frame
        manual_frame = min(manual_frame + 1, max_frames - 1)
        update(manual_frame)

    def prev_frame():
        nonlocal manual_frame
        manual_frame = max(manual_frame - 1, 0)
        update(manual_frame)

    def save_paths_button_action():
        save_updated_paths_txt(drones)
        print("[INFO] Updated paths saved.")

    def save_current_frame():
        save_dir = "/home/atom/uav_deconfliction/Plots/"
        os.makedirs(save_dir, exist_ok=True)
        filename = os.path.join(save_dir, f"frame_{manual_frame:03d}.png")
        fig.savefig(filename)
        print(f"[INFO] Current frame saved as {filename}")

    def re_route_drones():
        print("[AI] Re-routing started...")

        def is_conflict(p1, p2):
            return euclidean_distance_3d(p1, p2) < CONFLICT_DISTANCE

        def generate_new_path(drone_path, other_paths, drone_name):
            new_path = []
            visited = set()
            for t, point in enumerate(drone_path):
                candidate = point.copy()
                step = 1
                attempts = 0
                max_attempts = 30
                while any(
                    t < len(opath) and is_conflict(candidate, opath[t])
                    for opath in other_paths.values()
                ) or (candidate['x'], candidate['y'], candidate['z']) in visited:
                    candidate['z'] += np.random.choice([-step, step])
                    if attempts % 3 == 1:
                        candidate['x'] += np.random.choice([-step, step])
                    elif attempts % 3 == 2:
                        candidate['y'] += np.random.choice([-step, step])
                    visited.add((candidate['x'], candidate['y'], candidate['z']))
                    attempts += 1
                    if attempts > max_attempts:
                        print(f"[WARNING] Conflict not resolved at t={t} for {drone_name}")
                        break
                new_path.append(candidate)
                visited.add((candidate['x'], candidate['y'], candidate['z']))
            return new_path

        MAX_RETRIES = 20
        retry = 0
        success = False
        while retry < MAX_RETRIES:
            retry += 1
            print(f"[INFO] Attempt {retry} to generate conflict-free paths...")
            new_droneA = generate_new_path(drones['DroneA'], {'Primary': primary, 'DroneB': drones['DroneB']}, 'DroneA')
            new_droneB = generate_new_path(drones['DroneB'], {'Primary': primary, 'DroneA': new_droneA}, 'DroneB')

            drones['DroneA'] = new_droneA
            drones['DroneB'] = new_droneB

            new_conflicts = detect_conflicts(primary, drones)
            if not new_conflicts:
                success = True
                break
            else:
                print(f"[INFO] Conflicts still exist after attempt {retry}. Retrying...")

        if success:
            print("[SUCCESS] Conflict-free paths generated.")
        else:
            print("[WARNING] Could not generate conflict-free paths after multiple attempts.")

        nonlocal conflicts
        conflicts.clear()
        conflicts.extend(detect_conflicts(primary, drones))
        update(0)

    root = tk.Tk()
    root.wm_title("3D UAV Path Animation")

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_zlim(0, 100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Primary Drone Path
    p_x = [p['x'] for p in primary]
    p_y = [p['y'] for p in primary]
    p_z = [p['z'] for p in primary]
    p_line, = ax.plot([], [], [], color='blue', label='Primary Drone')

    drone_lines = {}
    drone_markers = {}
    for name, path in drones.items():
        line_color = 'green' if name == "DroneA" else 'orange'
        marker_color = 'green' if name == "DroneA" else 'purple'
        drone_lines[name], = ax.plot([], [], [], linestyle='--', color=line_color, label=name)
        drone_markers[name], = ax.plot([], [], [], marker='o', linestyle='', color=marker_color, label=f"{name} Pos")

    red_dots = ax.scatter([], [], [], c='red', marker='x', s=40, label='Conflict')
    conflict_texts = []
    time_text = ax.text2D(0.05, 0.95, "", transform=ax.transAxes)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # --- Test Case Buttons Frame ---
    test_case_frame = tk.Frame(root)
    test_case_frame.pack(side=tk.BOTTOM, fill=tk.X)

    def load_test_case(case_number):
        path_prefix = f"/home/atom/uav_deconfliction/mission_data/test_case{case_number}"
        primary_path = os.path.join(path_prefix, "primary_mission.json")
        droneA_path = os.path.join(path_prefix, "droneA.json")
        droneB_path = os.path.join(path_prefix, "droneB.json")

        try:
            new_primary = load_mission(primary_path)
            new_droneA = load_mission(droneA_path)
            new_droneB = load_mission(droneB_path)
        except Exception as e:
            print(f"[ERROR] Failed to load test case {case_number}: {e}")
            return

        nonlocal primary, drones, conflicts, max_frames
        primary[:] = new_primary
        drones["DroneA"][:] = new_droneA
        drones["DroneB"][:] = new_droneB

        max_frames = max(len(primary), *(len(p) for p in drones.values()))
        conflicts[:] = detect_conflicts(primary, drones)

        print(f"[INFO] Loaded Test Case {case_number}. Total Time Steps: {max_frames}")
        for t, loc, drone_id in conflicts:
            try:
                x = float(loc['x'])
                y = float(loc['y'])
                z = float(loc['z'])
                print(f"Conflict at ({x:.2f}, {y:.2f}, {z:.2f}) at t={t} with {drone_id}")
            except (ValueError, TypeError, KeyError) as e:
                print(f"[ERROR] Invalid conflict location at t={t} with {loc}: {drone_id} — {e}")
        update(0)

    # --- Test Case Buttons Frame (Now BELOW Control Buttons) ---
    test_case_frame = tk.Frame(root)
    test_case_frame.pack(side=tk.BOTTOM, fill=tk.X)

    tk.Label(test_case_frame, text="Load Test Case:").pack(side=tk.LEFT, padx=5)

    tk.Button(test_case_frame, text="Test Case 1", command=lambda: load_test_case(1),
          bg='#800080', fg='white').pack(side=tk.LEFT, padx=5)

    tk.Button(test_case_frame, text="Test Case 2", command=lambda: load_test_case(2),
          bg='#800080', fg='white').pack(side=tk.LEFT, padx=5)

    tk.Button(test_case_frame, text="Test Case 3", command=lambda: load_test_case(3),
          bg='#800080', fg='white').pack(side=tk.LEFT, padx=5)

    # --- Control Buttons Frame ---
    control_frame = tk.Frame(root)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X)

    tk.Button(control_frame, text="Start Animation", command=start_animation,
          bg='green', fg='white').pack(side=tk.LEFT, padx=5, pady=10)

    tk.Button(control_frame, text="Previous", command=prev_frame).pack(side=tk.LEFT, padx=5)

    tk.Button(control_frame, text="Next", command=next_frame).pack(side=tk.LEFT, padx=5)

    tk.Button(control_frame, text="Re-route with AI", command=re_route_drones,
          bg='blue', fg='white').pack(side=tk.LEFT, padx=5)

    tk.Button(control_frame, text="Save Updated Paths", command=save_paths_button_action,
          bg='yellow', fg='black').pack(side=tk.LEFT, padx=5)

    tk.Button(control_frame, text="Save Plot", command=save_current_frame,
          bg='white', fg='black').pack(side=tk.LEFT, padx=5)

    tk.Button(control_frame, text="Quit", command=stop_program,
          bg='red', fg='white').pack(side=tk.RIGHT, padx=5)

    
    max_frames = max(len(primary), *(len(p) for p in drones.values()))
    root.mainloop()

if __name__ == "__main__":
    primary = load_mission("mission_data/primary_mission.json")
    droneA = load_mission("mission_data/droneA.json")
    droneB = load_mission("mission_data/droneB.json")
    simulated_drones = {"DroneA": droneA, "DroneB": droneB}

    conflicts = detect_conflicts(primary, simulated_drones)
    for t, p, d in conflicts:
        print(f"Conflict at ({p['x']:.2f}, {p['y']:.2f}, {p['z']:.2f}) at t={t} with {d}")

    animate_paths(primary, simulated_drones, conflicts)

