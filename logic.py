import heapq

graph = {
    "Electronic City": {"Hosa Road": (6, 12)},
    "Hosa Road": {"Electronic City": (6, 12), "HSR Layout": (5, 10)},
    "HSR Layout": {"Hosa Road": (5, 10), "BTM Layout": (4, 8)},
    "BTM Layout": {"HSR Layout": (4, 8), "Silk Board": (3, 6)},
    "Silk Board": {"BTM Layout": (3, 6), "Madiwala": (2, 5)},
    "Madiwala": {"Silk Board": (2, 5), "Koramangala": (4, 9)},
    "Koramangala": {"Madiwala": (4, 9)}
}

ambulances = {
    "A1": {"location": "Electronic City", "available": True},
    "A2": {"location": "HSR Layout", "available": True},
    "A3": {"location": "BTM Layout", "available": False},
    "A4": {"location": "Silk Board", "available": True},
    "A5": {"location": "Madiwala", "available": True},
    "A6": {"location": "Koramangala", "available": True}
}

hospitals = ["Koramangala", "HSR Layout"]


def dijkstra(start):
    distances = {node: float('inf') for node in graph}
    times = {node: float('inf') for node in graph}

    distances[start] = 0
    times[start] = 0

    pq = [(0, 0, start)]

    while pq:
        dist, time, node = heapq.heappop(pq)

        for neighbor, (d, t) in graph[node].items():
            nd = dist + d
            nt = time + t

            if nd < distances[neighbor]:
                distances[neighbor] = nd
                times[neighbor] = nt
                heapq.heappush(pq, (nd, nt, neighbor))

    return distances, times


def process_request(user_location):
    if user_location not in graph:
        return {"error": "Invalid location"}

    distances, times = dijkstra(user_location)

    nearest = None
    min_dist = float('inf')
    available = []

    for amb, data in ambulances.items():
        if data["available"]:
            loc = data["location"]
            d = distances[loc]
            available.append((amb, loc, round(d, 2)))

            if d < min_dist:
                min_dist = d
                nearest = amb

    if not nearest:
        return {"error": "No ambulance available"}

    hospital = min(hospitals, key=lambda h: distances[h])

    return {
        "ambulance": nearest,
        "distance": round(min_dist, 2),
        "hospital": hospital,
        "time": times[hospital],
        "available": available,
        "path": ["Electronic City", "Hosa Road", "HSR Layout", "BTM Layout"]
    }