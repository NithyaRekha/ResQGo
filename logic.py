import heapq
import random
import math

# ---------------- GRAPH ----------------
graph = {
    "Electronic City": {"Hosa Road": (6, 12)},
    "Hosa Road": {"Electronic City": (6, 12), "HSR Layout": (5, 10)},
    "HSR Layout": {"Hosa Road": (5, 10), "BTM Layout": (4, 8)},
    "BTM Layout": {"HSR Layout": (4, 8), "Silk Board": (3, 6)},
    "Silk Board": {"BTM Layout": (3, 6), "Madiwala": (2, 5)},
    "Madiwala": {"Silk Board": (2, 5), "Koramangala": (4, 9)},
    "Koramangala": {"Madiwala": (4, 9)}
}

# ---------------- AMBULANCES ----------------
ambulances = [
    {"id": "AMB101", "driver": "Ramesh", "loc": "Electronic City Phase 1", "speed": 42, "available": True},
    {"id": "AMB102", "driver": "Suresh", "loc": "Koramangala", "speed": 38, "available": True},
    {"id": "AMB103", "driver": "Kiran", "loc": "Whitefield", "speed": 48, "available": True},
    {"id": "AMB104", "driver": "Mahesh", "loc": "Jayanagar", "speed": 35, "available": True},
    {"id": "AMB105", "driver": "Deepak", "loc": "Yelahanka", "speed": 44, "available": True},
    {"id": "AMB106", "driver": "Vijay", "loc": "Rajajinagar", "speed": 40, "available": True},
]

# ---------------- DIJKSTRA ----------------
def dijkstra(start):
    distances = {node: float('inf') for node in graph}
    times = {node: float('inf') for node in graph}

    distances[start] = 0
    times[start] = 0

    pq = [(0, 0, start)]

    while pq:
        dist, time, node = heapq.heappop(pq)

        if node not in graph:
            continue

        for neighbor, (d, t) in graph[node].items():
            nd = dist + d
            nt = time + t

            if nd < distances.get(neighbor, float('inf')):
                distances[neighbor] = nd
                times[neighbor] = nt
                heapq.heappush(pq, (nd, nt, neighbor))

    return distances, times

# ---------------- LOCATION MAPPING ----------------
def normalize_location(loc):
    loc = loc.lower()

    if "electronic" in loc:
        return "Electronic City"
    if "hsr" in loc:
        return "HSR Layout"
    if "btm" in loc:
        return "BTM Layout"
    if "koramangala" in loc:
        return "Koramangala"
    if "silk" in loc:
        return "Silk Board"
    if "madiwala" in loc:
        return "Madiwala"

    return None

# ---------------- ETA CALC ----------------
def calculate_eta(distance, speed):
    if speed == 0:
        return 999
    base = (distance / speed) * 60
    traffic = random.uniform(1.0, 1.6)
    return round(base * traffic, 2)

# ---------------- MAIN REQUEST ENGINE ----------------
def process_request(user_location):

    start = normalize_location(user_location)

    if not start:
        return {"error": "Invalid location detected"}

    distances, times = dijkstra(start)

    best = None
    best_score = float('inf')

    for amb in ambulances:

        if not amb["available"]:
            continue

        amb_loc = normalize_location(amb["loc"])
        if not amb_loc:
            continue

        if amb_loc not in distances:
            continue

        dist = distances[amb_loc]
        eta = calculate_eta(dist, amb["speed"])

        # SMART SCORE (important for hackathon)
        score = (dist * 0.6) + (eta * 0.4)

        if score < best_score:
            best_score = score
            best = amb

    if not best:
        return {"error": "No ambulance available"}

    best["available"] = False

    return {
        "ambulance_id": best["id"],
        "driver": best["driver"],
        "hospital": "Nearest Hospital Assigned",
        "distance": round(best_score, 2),
        "eta": f"{random.randint(6, 12)} mins",
        "status": "Ambulance Assigned"
    }

# ---------------- NEARBY AMBULANCES (OLA STYLE) ----------------
def nearby_ambulances(user_location, limit=3):

    start = normalize_location(user_location)

    if not start:
        return []

    distances, _ = dijkstra(start)

    result = []

    for amb in ambulances:

        amb_loc = normalize_location(amb["loc"])
        if not amb_loc:
            continue

        if amb_loc in distances:
            result.append({
                "id": amb["id"],
                "driver": amb["driver"],
                "distance": round(distances[amb_loc], 2),
                "available": amb["available"]
            })

    result.sort(key=lambda x: x["distance"])

    return result[:limit]