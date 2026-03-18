from collections import deque
from dataclasses import dataclass, field
import time
from Models import Edge
from data_structures.Triangulation import Triangulation

@dataclass
class StepData:
  flip_set: list[Edge]
  maximal_set: bool

@dataclass
class SearchState:
  tri: Triangulation
  path: list[StepData] = field(default_factory=list)

def exhaustive_simultanious_flip_graph_search(
  source: Triangulation,
  target: Triangulation,
  ignore_happy_edges: bool = False,
  enable_caching: bool = False,
  timeout: float = 600.0
) -> tuple[list[list[StepData]] | None, bool]: # returns (list of paths, did_timeout)
  if source == target:
    return [[]], False
  start_time = time.time()
  target_edges_set = target.edge_set()
  #BFS: each entry is a SearchState
  #visited: maps triangulation hashes to the depth at which they were first seen
  visited: dict[int, int] = {hash(source): 0}
  queue: deque[SearchState] = deque()
  queue.append(SearchState(source, []))
  results: list[list[StepData]] = []
  optimal_depth: int | None = None
  check_timeout_interval = 100
  iterations = 0
  while queue:
    iterations += 1
    if iterations % check_timeout_interval == 0:
      if time.time() - start_time > timeout:
        return (results if results else None, True)
    current_node = queue.popleft()
    current_tri, path = current_node.tri, current_node.path
    # If we already found optimal solutions, skip states deeper than optimal
    if optimal_depth is not None and len(path) >= optimal_depth:
      break
    flip_sets = current_tri.get_independent_flip_sets(target_edges_set if ignore_happy_edges else None)
    # precompute flippable edges and their face pairs for maximal check
    flippable = current_tri.get_flippable_edges()
    if ignore_happy_edges and target_edges_set:
      ignored_normalized = set(map(lambda e: (min(e[0], e[1]), max(e[0], e[1])), target_edges_set))
      flippable = [e for e in flippable if e not in ignored_normalized]
    edge_face_map: dict[Edge, tuple[int, int]] = {}
    for v1, v2 in flippable:
      he = current_tri.find_edge_by_ids(v1, v2)
      edge_face_map[(v1, v2)] = (he.face.id, he.twin.face.id)
    for flip_set in flip_sets:
      # check if flip_set is maximal: no flippable edge outside the set can be added
      used_faces: set[int] = set()
      flip_set_normalized = set(map(lambda e: (min(e[0], e[1]), max(e[0], e[1])), flip_set))
      for e in flip_set_normalized:
        fa, fb = edge_face_map[e]
        used_faces.add(fa)
        used_faces.add(fb)
      maximal_set = all(
        edge_face_map[e][0] in used_faces or edge_face_map[e][1] in used_faces
        for e in edge_face_map if e not in flip_set_normalized
      )
      neighbor = current_tri.deep_copy()
      neighbor.flip_edges_simultaneous(flip_set)
      if neighbor == target:
        result_path = path + [StepData(flip_set, maximal_set)]
        results.append(result_path)
        optimal_depth = len(result_path)
        continue
      h = hash(neighbor)
      new_depth = len(path) + 1
      if not enable_caching:
        # Allow revisiting states at the same depth to find all paths
        if h not in visited or visited[h] >= new_depth:
          visited[h] = new_depth
          queue.append(SearchState(neighbor, path + [StepData(flip_set, maximal_set)]))
      else:
        if h not in visited:
          visited[h] = new_depth
          queue.append(SearchState(neighbor, path + [StepData(flip_set, maximal_set)]))
  return (results if results else None, False)