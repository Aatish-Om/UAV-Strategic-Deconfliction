# UAV Strategic Deconfliction in Shared Airspace

## Overview

This project simulates multiple UAVs flying in a shared 3D airspace and detects potential conflicts (spatial and temporal) between their trajectories. The system supports AI-based rerouting to resolve conflicts and includes a GUI for visualizing UAV paths and managing the simulation.

## Features

- Modular architecture (data ingestion, conflict detection, simulation, visualization)
- 4D conflict detection (3D space + time)
- AI logic for rerouting conflicting UAVs
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
├── main.py                     # Entry point: launches GUI and simulator
├── requirements.txt            # Dependencies for environment setup
├── mission_data/              # Organized folders of input mission JSONs
│   ├── default/
│   ├── test_case1/
│   ├── test_case2/
│   └── test_case3/
├── Plots/                     # Output plots and animation frames
├── utils/                     # Utility modules
│   ├── deconflictor.py        # Core logic for conflict detection
│   ├── parser.py              # Data ingestion and validation
│   ├── simulator.py           # Trajectory simulation and AI rerouting
│   └── visualizer.py          # 3D and 4D visualization logic
├── venv/                      # Virtual environment
└── README.md
```

## Running the Simulation

1. Clone the repository or download the folder.
2. Ensure all dependencies are installed.
3. Run the GUI with:

```bash
source venv/bin/activate
python main.py
```

4. Use the GUI to:
![image](https://github.com/user-attachments/assets/e708b6d4-1ab3-4abc-bd32-def7d581aab5)

![image](https://github.com/user-attachments/assets/4050b964-b425-48ab-a7ce-8f109ad4b711)

   - Load mission data from `mission_data/`
   - Run the simulation frame-by-frame or automatically
   - Detect and visualize conflicts
   - Apply rerouting strategies
   - Save rerouted path plots to `Plots/`

## Test Cases

- `mission_data/test_case1`: Vertical conflict
  
![image](https://github.com/user-attachments/assets/9572027a-3731-4692-b0de-4d0e50814920)

![image](https://github.com/user-attachments/assets/0076b962-b1a7-4c3b-a89b-c23a75d0d579)

- `mission_data/test_case2`: Path intersection
  
![image](https://github.com/user-attachments/assets/94ad89cb-57fb-4181-b311-67a0baf0698c)

![image](https://github.com/user-attachments/assets/8f59bad0-6e4c-4d0d-9a25-1ab7e9301d0e)

- `mission_data/test_case3`: Parallel path proximity
  
![image](https://github.com/user-attachments/assets/4410012c-c255-4f8e-998c-9778486eeeff)

![image](https://github.com/user-attachments/assets/93112595-f53f-4e93-a247-b33c0afd9555)



Each file contains timestamped 3D trajectories of multiple drones.

## AI Conflict Resolution

Upon detecting a conflict:
- Attempts altitude change
- If unsuccessful, applies lateral rerouting
- Ensures separation is restored while preserving mission continuity

## Extra Features

- 4D visualization (space + time)
- Step-by-step conflict analysis
- User control for previous and save operations

## License

MIT License

## Author

Aatish Om – UAV Strategic Deconfliction System
