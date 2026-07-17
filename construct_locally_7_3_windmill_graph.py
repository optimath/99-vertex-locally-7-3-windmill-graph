"""Construct a 99-vertex locally (7, 3)-windmill graph using CP-SAT.

For every vertex, the graph induced by its open neighborhood is isomorphic to
7K2. Equivalently, the graph is 14-regular and every edge lies in exactly one
triangle.

The triangles are modeled as hyperedges of a 3-uniform, 3-partite linear
hypergraph. Tripartiteness is an additional constraint of this construction,
not part of the definition of a locally (7, 3)-windmill graph.
"""

from ortools.sat.python import cp_model

PART_SIZE = 33
NUM_VERTICES = 99
TRIANGLES_PER_VERTEX = 7
PART_A = range(0, 33)
PART_B = range(33, 66)
PART_C = range(66, 99)


def build_model():
    """Build and return the CP-SAT model and its decision variables."""
    model = cp_model.CpModel()
    triples = [(i, j, k) for i in PART_A for j in PART_B for k in PART_C]
    pairs_ab = [(i, j) for i in PART_A for j in PART_B]
    pairs_ac = [(i, k) for i in PART_A for k in PART_C]
    pairs_bc = [(j, k) for j in PART_B for k in PART_C]
    pairs = pairs_ab + pairs_ac + pairs_bc

    x = {t: model.NewBoolVar(f"x[{t}]") for t in triples}
    e = {p: model.NewBoolVar(f"e[{p}]") for p in pairs}

    # Link selected hyperedges (triangles) to graph edges.
    for i, j in pairs_ab:
        model.AddMaxEquality(e[(i, j)], [x[(i, j, k)] for k in PART_C])
    for i, k in pairs_ac:
        model.AddMaxEquality(e[(i, k)], [x[(i, j, k)] for j in PART_B])
    for j, k in pairs_bc:
        model.AddMaxEquality(e[(j, k)], [x[(i, j, k)] for i in PART_A])

    # Every graph vertex belongs to exactly seven selected triangles.
    for i in PART_A:
        model.Add(sum(x[(i, j, k)] for j, k in pairs_bc) == TRIANGLES_PER_VERTEX)
    for j in PART_B:
        model.Add(sum(x[(i, j, k)] for i, k in pairs_ac) == TRIANGLES_PER_VERTEX)
    for k in PART_C:
        model.Add(sum(x[(i, j, k)] for i, j in pairs_ab) == TRIANGLES_PER_VERTEX)

    # Linearity: every pair occurs in at most one selected hyperedge.
    for i, j in pairs_ab:
        model.Add(sum(x[(i, j, k)] for k in PART_C) <= 1)
    for i, k in pairs_ac:
        model.Add(sum(x[(i, j, k)] for j in PART_B) <= 1)
    for j, k in pairs_bc:
        model.Add(sum(x[(i, j, k)] for i in PART_A) <= 1)

    # Forbid additional graph triangles not represented by selected hyperedges.
    for i, j, k in triples:
        model.Add(e[(i, j)] + e[(i, k)] + e[(j, k)] <= 2).OnlyEnforceIf(
            x[(i, j, k)].Not()
        )

    return model, triples, x


def main():
    """Solve the model and print one feasible set of 231 triangles."""
    model, triples, x = build_model()
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("No solution found.")
        return

    selected = [triple for triple in triples if solver.Value(x[triple])]
    print(f"Selected triangles: {len(selected)}")
    for triangle in selected:
        print(*triangle)


if __name__ == "__main__":
    main()
