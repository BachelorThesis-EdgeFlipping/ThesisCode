# Simultaneous Flip Graph Search — Bachelor Thesis

This repository contains the implementation developed for a bachelor thesis on simultaneous edge flips in triangulation flip graphs. It includes the core data structure, the search algorithm, test instance generators, test executables, and visualization tools used to produce figures for the thesis.

## Requirements

```
pip install -r Requirements.txt
```

Python 3.10+ is required (type hints use newer syntax).

---

## Core Files

### Data Structure — `data_structures/Triangulation.py`

The central data structure of the entire project. Implements a triangulation as a **Doubly-Connected Edge List (DCEL)** with:

- `Vertex`, `HalfEdge`, `Face` — the low-level DCEL primitives
- `Triangulation` — the main class, supporting:
  - Initialization from a convex polygon (`initialize_regular_polygon`) or from an explicit edge list (`initialize_from_edges`)
  - Edge flipping: `flip_edge()`, `flip_edges_simultaneous()`, `is_flippable()`
  - Enumerating all **independent flip sets** (including all maximal ones) via `get_independent_flip_sets()`
  - Comparing two triangulations by shared edges / geometric crossings
  - A comprehensive `sanity_check()` that validates the DCEL invariants

### Algorithm — `ExhaustiveSearchAlgorithm.py`

Implements a **BFS-based exhaustive search** over the simultaneous-flip graph between two triangulations. The main function is:

```python
exhaustive_simultanious_flip_graph_search(source, target, flags...) -> (paths | None, did_timeout)
```

Key flags that control search behaviour:

| Flag | Effect |
|---|---|
| `ignore_happy_edges` | Skip edges already present in the target |
| `only_flip_maximal_sets` | Only explore maximal independent sets at each step |
| `only_flip_descreasing_intersection_score` | Prune paths that do not reduce the intersection score |
| `only_one_path_per_state` | Keep only one representative path per visited state |
| `only_single_flips` | Restrict to single-edge flips (classic flip graph) |
| `timeout` | Abort after 10 minutes and return `did_timeout=True` |

Returns the list of all optimal (shortest) paths found, or `None` if no solution exists within the timeout.

---

## Test Executables

Both executables accept either a **single pair** or a **suite** of pairs as input.

### `XExhaustiveSearch.py` — Main empirical evaluation

Runs the exhaustive search algorithm over a test suite and reports:
- Number of optimal paths and their length
- Per-path flip sequences (marking which steps use maximal sets)
- Equivalence classes of paths by total edge set
- Twin-pair statistics (suite mode): coverage, all-maximal path ratios, etc.

```
python XExhaustiveSearch.py <parser> <mode> <source> [target] [-log]
```

| Argument | Values | Description |
|---|---|---|
| `<parser>` | `-ps` / `-cp` | Point-set or convex-polygon triangulation format |
| `<mode>` | `-suite` / `-no_suite` | Run a whole suite or a single pair |
| `<source>` | suite name or file path | Suite name (relative to `data/suites/`) or source triangulation file |
| `[target]` | file path | Target triangulation file (only in `-no_suite` mode) |
| `[-log]` | optional flag | Write a crash-safe progress log to `test_results/logs/progress.log` |

**Suite example (convex polygon):**
```
python XExhaustiveSearch.py -cp -suite generated/cp_7_ALL_520652526_suite_n1722_twins
```

**Suite example (point set):**
```
python XExhaustiveSearch.py -ps -suite generated/6_25_ALL_849624902_suite_n1878_twins -log
```

Results are typically redirected to a file:
```
python XExhaustiveSearch.py -cp -suite generated/cp_7_ALL_520652526_suite_n1722_twins > test_results/from_generated/cp_rand7_result.txt
```

### `XCheckMISHypothesis.py` — Hypothesis test

A specialised variant that tests whether the **maximal-independent-set (MIS) hypothesis** holds: it runs the search with `only_flip_maximal_sets`, `only_flip_descreasing_intersection_score`, and `only_one_path_per_state` all enabled. If any pair has no solution under these constraints, the hypothesis is falsified and the run terminates early.

Usage mirrors `XExhaustiveSearch.py`:
```
python XCheckMISHypothesis.py <parser> <mode> <source> [target] [-log]
```

---

## Test Instance Generation

All generators are interactive CLIs — run them without arguments and follow the prompts.

### `GenerateConvexPolygonTriangulations.py`

Generates triangulations of a convex polygon with a given number of vertices.

- Mode **ALL**: discovers every distinct triangulation via BFS.
- Mode **N random**: samples N triangulations by applying random sequences of flips.

Output: JSON files in `data/convex_polygon/generated/<folder>/`.

```
python GenerateConvexPolygonTriangulations.py
```

### `GenerateRandomPointSetTriangulations.py`

Generates triangulations of random point sets.

- Starts from a Delaunay triangulation of a randomly sampled point set.
- Mode **ALL** or **N random** flips, same as above.

Output: JSON files in `data/point_set/generated/<folder>/`.

```
python GenerateRandomPointSetTriangulations.py
```

### `GenerateSuites.py`

Pairs up triangulations from a generated folder into a test suite.

- Generates all pairs or N random pairs per point set.
- Optionally produces **twin** pairs (each pair is included in both directions).

Output: a single JSON file in `data/suites/generated/` that lists source/target triangulation names. This file is then passed directly to `XExhaustiveSearch.py` or `XCheckMISHypothesis.py`.

```
python GenerateSuites.py
```

---

## Test Suites Used in the Thesis

The exact suites used for the empirical evaluation are listed in **`used_suites_for_thesis_results.txt`**. There are 22 suites in total, split into two groups:

- **Convex polygon** (`-cp`): polygon sizes 4 – 15 vertices
- **General point set** (`-ps`): point sets with 6 – 15 vertices

All suite files are located in `data/suites/generated/` and follow the naming pattern:

```
<type>_<size>_<flip-range>_<seed>_suite_n<count>_twins
```

Where `<count>` is the number of problem pairs and `_twins` means each pair appears in both directions.

---

## Visualization — `render_export/`

All modules and scripts used to generate figures for the thesis. `render_export/scripts/` contains individual render scripts (e.g. `XMISDecomposition.py`, `XHappyEdgeProgressFlip.py`) that produce Matplotlib figures. `render_export/GraphRenderer.py` is the shared rendering backend.

---

## Other Files

The repository also contains a **pygame-based interactive application** (`frontend/`), additional test executables (`XFindShortestPath.py`, `XFlipGraphAnalysis.py`, etc.), and various IO utilities — none of these were used in the thesis work and are not documented here.
