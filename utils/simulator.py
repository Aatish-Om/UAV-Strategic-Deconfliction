# utils/simulator.py
from utils.parser import load_mission
from utils.deconflictor import check_conflict

def run_simulation():
    primary = load_mission("mission_data/primary_mission.json")
    others = load_mission("mission_data/simulated_drones.json")

    conflicts = check_conflict(primary, others)
    if conflicts:
        return "Conflict Detected", conflicts
    else:
        return "Clear to Fly", []

