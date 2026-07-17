# A 99-Vertex Locally (7, 3)-Windmill Graph

This repository presents a Google OR-Tools CP-SAT construction of a
**99-vertex locally (7,3)-windmill graph**.

![Tripartite layout of the constructed graph](results/graph_tripartite_layout.png)
*Tripartite layout of the constructed 99-vertex locally (7,3)-windmill graph. The three colors represent the vertex parts of size 33.*

For every vertex, the graph induced by its open neighborhood is isomorphic to
7K<sub>2</sub>. Equivalently, the graph is 14-regular and every edge belongs to
exactly one triangle.

The constructed graph is additionally tripartite.

## Verified graph properties

- 99 vertices;
- 693 edges;
- 231 triangles;
- 14-regular;
- Connected;
- Diameter 3;
- Radius 3;
- Girth 3;
- Every edge belongs to exactly one triangle;
- Every open neighborhood is isomorphic to 7K<sub>2</sub>;
- Tripartite, with three parts of size 33;
- Contains an induced Paley graph P(9).

All these properties were checked directly from the stored graph.

## Repository contents

- `construct_locally_7_3_windmill_graph.py` — OR-Tools CP-SAT construction;
- `verify_graph.py` — independent verification of the stored graph;
- `results/adjacency_lists.txt` — primary representation of the graph;
- `results/graph_triangles.json` — the complete list of its 231 triangles;
- `results/graph.graphml` — GraphML file for yEd, Gephi, NetworkX, and similar software;
- `results/graph_properties.txt` — verified numerical and structural properties.

## Construction model

The triangles are represented as the hyperedges of a
**3-uniform, 3-partite linear hypergraph**. The vertex set is partitioned into three parts:

- **A** = {0, ..., 32}
- **B** = {33, ..., 65}
- **C** = {66, ..., 98}

Every selected hyperedge contains one vertex from each part. The model requires:

1. Every vertex to belong to exactly seven selected hyperedges;
2. Every pair of vertices to occur in at most one selected hyperedge;
3. Every hyperedge to define a graph triangle;
4. No additional graph triangles to occur.

The second condition is hypergraph linearity.

## Stored graph

The primary representation is `results/adjacency_lists.txt`. For example,

```text
0: 42 44 48 51 53 59 65 66 71 78 81 88 89 91
```

lists the 14 neighbors of vertex 0.

The file `results/graph_triangles.json` stores the same graph as 231 triples.
Each triple `[i, j, k]` represents a triangle on vertices `i`, `j`, and `k`.
The triangle list determines all 693 edges because every edge belongs to exactly
one triangle.

## Paley graph of order 9

The vertices

```text
{7, 8, 9, 34, 35, 53, 69, 71, 86}
```

induce a subgraph isomorphic to the Paley graph of order 9, equivalently the
3×3 rook graph. It is strongly regular with parameters
srg(9,4,1,2).

## Running the construction

```bash
pip install -r requirements.txt
python construct_locally_7_3_windmill_graph.py
```

The original Google Colab run found a feasible solution in approximately
40 minutes. Runtime depends on hardware, OR-Tools version, solver settings, and
randomization.

## Verifying the stored graph

```bash
python verify_graph.py
```

The verification script uses only the Python standard library.

## License

The source code and stored construction are released under the MIT License.
