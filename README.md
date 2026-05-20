# Simultaneous Flip Graph Search — Bachelor Thesis

This repository contains the implementation for a bachelor thesis on **simultaneous edge flips in triangulation flip graphs**. It includes the triangulation data structure, the exhaustive search algorithm, the test executables and their inputs, and the scripts used to produce the figures in the thesis.

## Setup

```
pip install -r Requirements.txt
```

Dependencies: `networkx`, `matplotlib`, `scipy`, `dataclasses-json`, `pygame` (the last only for the unused interactive app). Python 3.10+ is required.

---

## Repository map (only files relevant to the thesis)

| Path | Purpose |
|---|---|
| [data_structures/Triangulation.py](data_structures/Triangulation.py) | Core data structure — DCEL triangulation |
| [ExhaustiveSearchAlgorithm.py](ExhaustiveSearchAlgorithm.py) | The only algorithm used in the thesis |
| [XExhaustiveSearch.py](XExhaustiveSearch.py) | Test executable — main empirical evaluation |
| [XCheckMISHypothesis.py](XCheckMISHypothesis.py) | Test executable — MIS hypothesis check |
| [GenerateConvexPolygonTriangulations.py](GenerateConvexPolygonTriangulations.py) | Generator — convex polygon triangulations |
| [GenerateRandomPointSetTriangulations.py](GenerateRandomPointSetTriangulations.py) | Generator — point-set triangulations |
| [GenerateSuites.py](GenerateSuites.py) | Generator — problem pairs (suites) from triangulations |
| [render_export/](render_export/) | All figures used in the thesis are produced here |
| [used_suites_for_thesis_results.txt](used_suites_for_thesis_results.txt) | **List of the exact test suites evaluated in the thesis** |
| [data/suites/generated/](data/suites/generated/) | Generated suites (inputs to the test executables) |
| [data/convex_polygon/generated/](data/convex_polygon/generated/), [data/point_set/generated/](data/point_set/generated/) | Generated triangulations referenced by the suites |

Everything else in the repository (the `frontend/` pygame app, the `X*.py` files not listed above, the `io_utils/`, the additional rendering helpers) was **not** used for the thesis.

---

## Core data structure — [data_structures/Triangulation.py](data_structures/Triangulation.py)

The central data structure of the entire project. A triangulation is represented as a **Doubly-Connected Edge List (DCEL)** built from `Vertex`, `HalfEdge`, and `Face`. The `Triangulation` class supports:

- Initialization from a convex polygon (`initialize_regular_polygon`) or from an explicit point/edge list (`initialize_from_edges`)
- Edge flipping: `flip_edge`, `flip_edges_simultaneous`, `is_flippable`
- Enumeration of all independent flip sets, including all maximal ones, via `get_independent_flip_sets`
- Comparison between two triangulations by shared edges and geometric crossings
- A `sanity_check` that verifies all DCEL invariants (Euler's formula, twin/next/prev consistency, face consistency)

## Core algorithm — [ExhaustiveSearchAlgorithm.py](ExhaustiveSearchAlgorithm.py)

A **BFS over the simultaneous-flip graph** between a source and a target triangulation. Returns *all* optimal (shortest) paths, or `None` if the timeout (default 10 min) is reached.

```python
exhaustive_simultanious_flip_graph_search(
    source: Triangulation,
    target: Triangulation,
    ignore_happy_edges: bool = False,
    only_flip_maximal_sets: bool = False,
    only_flip_descreasing_intersection_score: bool = False,
    never_flip_positive_intersection_score_for_individual_flips: bool = False,
    only_one_path_per_state: bool = False,
    only_single_flips: bool = False,
    timeout: float = 600.0,
) -> tuple[list[list[StepData]] | None, bool]   # (paths, did_timeout)
```

The flags select the pruning strategy used by the search. The two test executables below set these flags differently.

---

## Running the tests

Both test executables share the same CLI:

```
python <executable>.py <parser> <mode> <suite-or-source> [target] [-log]
```

| Argument | Values | Description |
|---|---|---|
| `<parser>` | `-cp` / `-ps` | Convex polygon or general point-set format |
| `<mode>` | `-suite` / `-no_suite` | Run a whole suite of pairs, or one pair |
| `<suite-or-source>` | suite name *or* triangulation file path | In `-suite` mode: the suite name (relative to `data/suites/`). In `-no_suite` mode: the source triangulation file |
| `[target]` | triangulation file path | Required only in `-no_suite` mode |
| `[-log]` | optional flag | Writes a crash-safe progress log to `test_results/logs/progress.log` |

### [XExhaustiveSearch.py](XExhaustiveSearch.py) — main empirical evaluation

Runs the unconstrained exhaustive search on every pair in a suite and reports, per pair: the number of optimal paths, their length, the per-step flip sets (with a flag for maximal sets), the equivalence classes by total edge set. In suite mode, it additionally aggregates twin-pair statistics and the share of all-maximal optimal paths.

**Reproducing a thesis result** (e.g. convex polygons with 7 vertices):

```
python XExhaustiveSearch.py -cp -suite generated/cp_7_ALL_520652526_suite_n1722_twins > test_results/from_generated/cp_rand7_result.txt
```

**Point-set example** with progress log:

```
python XExhaustiveSearch.py -ps -suite generated/6_25_ALL_849624902_suite_n1878_twins -log > test_results/from_generated/ps_rand6_result.txt
```

### [XCheckMISHypothesis.py](XCheckMISHypothesis.py) — MIS hypothesis check

A specialised variant that runs the search with the three flags
`only_flip_maximal_sets`, `only_flip_descreasing_intersection_score`, and
`only_one_path_per_state` all enabled. If any pair has no solution under these constraints, the **maximal-independent-set hypothesis** is falsified and the run terminates early.

```
python XCheckMISHypothesis.py -cp -suite generated/cp_7_ALL_520652526_suite_n1722_twins
```

### Which suites were used in the thesis?

The exact 22 suites used for the empirical evaluation are listed in **[used_suites_for_thesis_results.txt](used_suites_for_thesis_results.txt)**:

- **Convex polygon** (`-cp`): 12 suites, polygon sizes 4 – 15
- **General point set** (`-ps`): 10 suites, point sets of size 6 – 15

Suite filenames follow the pattern `<type>_<size>_<flip-range>_<seed>_suite_n<count>_twins`, where `<count>` is the number of problem pairs and `_twins` means each pair is included in both directions.

---

## Generating new test data

All three generators are interactive — run them without arguments and answer the prompts.

| Script | Output location | What it generates |
|---|---|---|
| [GenerateConvexPolygonTriangulations.py](GenerateConvexPolygonTriangulations.py) | `data/convex_polygon/generated/<folder>/` | Triangulations of a convex polygon (mode `ALL` enumerates every distinct one; mode `N random` samples via random flip sequences) |
| [GenerateRandomPointSetTriangulations.py](GenerateRandomPointSetTriangulations.py) | `data/point_set/generated/<folder>/` | Triangulations of random point sets, starting from a Delaunay triangulation; same `ALL` / `N random` modes |
| [GenerateSuites.py](GenerateSuites.py) | `data/suites/generated/<name>.json` | Pairs up generated triangulations into a suite (all pairs or N random pairs per point set; optional `_twins` produces each pair in both directions) |

The output of `GenerateSuites.py` is exactly what the two test executables consume as their `-suite` argument.

---

## Figures — [render_export/](render_export/)

All figures shown in the thesis are produced by the scripts in [render_export/scripts/](render_export/scripts/) (e.g. `XMISDecomposition.py`, `XHappyEdgeProgressFlip.py`, `XCappedChannels.py`). The shared rendering backend is [render_export/GraphRenderer.py](render_export/GraphRenderer.py); colours and styling helpers live alongside it.

---

## Not used for the thesis

The repository also contains a pygame-based interactive application (`frontend/`), several additional `X*.py` executables, and a few I/O helpers — none of these were used for the thesis and they can be ignored when reviewing.
