# UAV Strategic Deconfliction in Shared Airspace

## Overview

This project simulates multiple UAVs flying in a shared 3D airspace and detects potential conflicts (spatial and temporal) between their trajectories. The system supports AI-based rerouting to resolve conflicts and includes a GUI for visualizing UAV paths and managing the simulation.

## Features

- Modular architecture (data ingestion, conflict detection, simulation, visualization)
- 4D conflict detection (3D space + time)
- Simple AI logic for rerouting conflicting UAVs
- GUI for path loading, animation, and control
- Saves rerouted paths and conflict plots

## Requirements

- Python 3.8 or higher
- Packages:
  - matplotlib
  - tkinter (comes with Python by default)

To install required packages:

```bash
pip install matplotlib
```

## Project Structure

```
uav_deconfliction/
├── main.py               # Main GUI and simulation controller
├── parser.py             # Parses UAV mission data from JSON
├── deconflictor.py       # Conflict detection logic (spatial + temporal)
├── simulator.py          # Rerouting and flight update logic
├── visualizer.py         # 3D visualization and animation
├── utils/                # Utility scripts
├── mission_data/         # Test case folders with JSON files
├── Plots/                # Saved images of simulations
└── README.md
```

## Running the Simulation

1. Clone the repository or download the folder.
2. Ensure all dependencies are installed.
3. Run the GUI with:

```bash
python main.py
```

4. Use the GUI to:
   - Load mission data from `mission_data/`
   - Run the simulation frame-by-frame or automatically
   - Detect and visualize conflicts
   - Apply rerouting strategies
   - Save rerouted path plots to `Plots/`

## Test Cases

- `mission_data/case1.json`: Vertical conflict
- `mission_data/case2.json`: Path intersection
- `mission_data/case3.json`: Parallel path proximity

Each file contains timestamped 3D trajectories of multiple drones.

## AI Conflict Resolution

Upon detecting a conflict:
- Attempts altitude change
- If unsuccessful, applies lateral rerouting
- Ensures separation is restored while preserving mission continuity

## Extra Features

- 4D visualization (space + time)
- Step-by-step conflict analysis
- User control for pause, resume, and save operations

## License

MIT License

## Author

[Your Name] – UAV Strategic Deconfliction System
