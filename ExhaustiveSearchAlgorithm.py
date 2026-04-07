from collections import deque
from dataclasses import dataclass, field
import time
import gc
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
  only_flip_maximal_sets: bool = False,
  only_flip_descreasing_intersection_score: bool = False,
  never_flip_positive_intersection_score_flips: bool = False,
  only_one_path_per_state: bool = False,
  timeout: float = 600.0
) -> tuple[list[list[StepData]] | None, bool]: # returns (list of paths, did_timeout)
  source_vertices = tuple(sorted((v.x, v.y) for v in source.vertices))
  target_vertices = tuple(sorted((v.x, v.y) for v in target.vertices))
  if source_vertices != target_vertices:
    raise ValueError("Source and target triangulations are not compatible (they do not share the same set of vertices).")

  if source == target:
    return [[]], False
  start_time = time.time()
  target_edges_set = target.edge_set()
  #BFS: each entry is a SearchState
  #visited: maps triangulation hashes to a tuple of (depth, represents_an_all_maximal_path)
  visited: dict[int, tuple[int, bool]] = {hash(source): (0, True)}
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
        for node in queue:
          if node.tri is not source and node.tri is not target:
            node.tri.destroy()
        queue.clear()
        gc.collect()
        return (results if results else None, True)
    current_node = queue.popleft()
    current_tri, path = current_node.tri, current_node.path
    if only_one_path_per_state and path:
      is_path_all_maximal = all(step.maximal_set for step in path)
      if not is_path_all_maximal and visited[hash(current_tri)][1]:
        if current_tri is not source and current_tri is not target:
          current_tri.destroy()
        continue
    
    old_crossing_score = (
      current_tri.count_geometric_crossings_with(target)
      if only_flip_descreasing_intersection_score or never_flip_positive_intersection_score_flips
      else None
    )
    per_edge_negative_cache: dict[Edge, bool] = {}
    # If we already found optimal solutions, skip states deeper than optimal
    if optimal_depth is not None and len(path) >= optimal_depth:
      if current_tri is not source and current_tri is not target:
        current_tri.destroy()
      continue
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
      if only_flip_maximal_sets and not maximal_set:
        continue #skip flipping non-maximal sets if we are only interested in MIS
      neighbor = current_tri.deep_copy()
      if never_flip_positive_intersection_score_flips and old_crossing_score is not None:
        only_crossing_score_decrease = True
        previous_crossing_score = old_crossing_score
        for edge in sorted(flip_set_normalized):
          can_flip_step = neighbor.flip_edge(edge[0], edge[1])
          if not can_flip_step:
            neighbor.destroy()
            raise Exception(f"Edge {edge} was expected to be flippable but is not. This should not happen.")
          next_crossing_score = neighbor.count_geometric_crossings_with(target)
          if next_crossing_score > previous_crossing_score:
            only_crossing_score_decrease = False
            break
          previous_crossing_score = next_crossing_score
        if not only_crossing_score_decrease:
          neighbor.destroy()
          continue # skip sets that do not monotonically decrease the crossing score at each individual flip
      else:
        neighbor.flip_edges_simultaneous(flip_set)
      if only_flip_descreasing_intersection_score:
        new_score = neighbor.count_geometric_crossings_with(target)
        if old_crossing_score is not None and new_score >= old_crossing_score:
          neighbor.destroy()
          continue #skip flips that do not decrease the intersection score if we are only interested in those
      if neighbor == target:
        result_path = path + [StepData(flip_set, maximal_set)]
        results.append(result_path)
        optimal_depth = len(result_path)
        neighbor.destroy()
        continue
      h = hash(neighbor)
      new_depth = len(path) + 1
      is_all_maximal = maximal_set and all(step.maximal_set for step in path)
      if not only_one_path_per_state:
        # Allow revisiting states at the same depth to find all paths possible
        if h not in visited or visited[h][0] >= new_depth:
          visited[h] = (new_depth, visited[h][1] or is_all_maximal if h in visited else is_all_maximal)
          queue.append(SearchState(neighbor, path + [StepData(flip_set, maximal_set)]))
        else:
          neighbor.destroy()
      else:
        if h not in visited:
          visited[h] = (new_depth, is_all_maximal)
          queue.append(SearchState(neighbor, path + [StepData(flip_set, maximal_set)]))
        elif visited[h][0] == new_depth and not visited[h][1] and is_all_maximal:
          # We previously arrived at this state with a non all-maximal path, but now we have an all-maximal one.
          visited[h] = (new_depth, True)
          queue.append(SearchState(neighbor, path + [StepData(flip_set, maximal_set)]))
        else:
          neighbor.destroy()
    if current_tri is not source and current_tri is not target:
      current_tri.destroy()
  gc.collect()
  return (results if results else None, False)