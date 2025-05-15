# utils/deconflictor.py
import numpy as np

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def check_conflict(primary, others, buffer_dist=10.0):
    conflicts = []
    for other in others:
        for p_wp in primary['waypoints']:
            for o_wp in other['waypoints']:
                dist = euclidean(p_wp['pos'], o_wp['pos'])
                if dist <= buffer_dist and p_wp['time'] == o_wp['time']:
                    conflicts.append({
                        "location": p_wp['pos'],
                        "time": p_wp['time'],
                        "with_drone": other['id']
                    })
    return conflicts

