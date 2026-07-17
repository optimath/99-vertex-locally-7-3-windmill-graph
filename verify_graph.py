"""Verify the stored 99-vertex graph and print its main properties."""

import json
from collections import Counter, deque
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRIANGLES_FILE = ROOT / "results" / "graph_triangles.json"


def load_graph():
    triangles = [tuple(t) for t in json.loads(TRIANGLES_FILE.read_text())]
    adjacency = [set() for _ in range(99)]
    edge_multiplicity = Counter()
    for a, b, c in triangles:
        for u, v in ((a, b), (a, c), (b, c)):
            edge = tuple(sorted((u, v)))
            edge_multiplicity[edge] += 1
            adjacency[u].add(v)
            adjacency[v].add(u)
    return triangles, adjacency, edge_multiplicity


def distances_from(source, adjacency):
    distance = [-1] * len(adjacency)
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


def main():
    triangles, adjacency, multiplicity = load_graph()
    all_distances = [distances_from(v, adjacency) for v in range(99)]
    connected = all(d >= 0 for row in all_distances for d in row)
    diameter = max(max(row) for row in all_distances)
    radius = min(max(row) for row in all_distances)

    graph_triangles = []
    for a, b, c in combinations(range(99), 3):
        if b in adjacency[a] and c in adjacency[a] and c in adjacency[b]:
            graph_triangles.append((a, b, c))

    local_ok = True
    for v in range(99):
        neighborhood = adjacency[v]
        local_degrees = [len(adjacency[u] & neighborhood) for u in neighborhood]
        local_ok &= len(neighborhood) == 14 and local_degrees == [1] * 14

    print(f"Vertices: {len(adjacency)}")
    print(f"Edges: {len(multiplicity)}")
    print(f"Triangles: {len(graph_triangles)}")
    print(f"14-regular: {all(len(n) == 14 for n in adjacency)}")
    print(f"Connected: {connected}")
    print(f"Diameter: {diameter}")
    print(f"Radius: {radius}")
    print(f"Every edge in exactly one triangle: {set(multiplicity.values()) == {1}}")
    print(f"Every open neighborhood is 7K2: {local_ok}")
    print(f"Stored triangles are all graph triangles: {set(graph_triangles) == set(map(tuple, triangles))}")


if __name__ == "__main__":
    main()
