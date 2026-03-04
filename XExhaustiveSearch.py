import sys
from collections import deque
from dataclasses import dataclass, field

from data_structures.Triangulation import Triangulation
from Models import Edge
from io_utils.PointSetTriangulationParser import PointSetTriangulationParser

@dataclass
class StepData:
  flip_set: list[Edge]
  maximum_set: bool

@dataclass
class SearchState:
  tri: Triangulation
  path: list[StepData] = field(default_factory=list)

def exhaustive_simultanious_flip_graph_search(
  source: Triangulation,
  target: Triangulation,
  ignore_happy_edges: bool = False
) -> list[list[Edge]] | None:
  if source == target:
    return []
  target_edges_set = target.edge_set()
  #BFS: each entry is a SearchState
  #visited for caching triangulation hashes to avoid revisiting
  visited: set[int] = {hash(source)}
  queue: deque[SearchState] = deque()
  queue.append(SearchState(source, []))
  while queue:
    current_node = queue.popleft()
    current_tri, path = current_node.tri, current_node.path
    flip_sets = current_tri.get_independent_flip_sets(target_edges_set if ignore_happy_edges else None)
    flip_sets_max_size = len(flip_sets[0]) if flip_sets else 0
    for flip_set in flip_sets:
      maximum_set = len(flip_set) == flip_sets_max_size
      neighbor = current_tri.deep_copy()
      neighbor.flip_edges_simultaneous(flip_set)
      if neighbor == target:
        return path + [StepData(flip_set, maximum_set)]
      h = hash(neighbor)
      if h not in visited:
        visited.add(h)
        queue.append(SearchState(neighbor, path + [StepData(flip_set, maximum_set)]))
  return None

############
#   main   #
############
source_file = f"{sys.argv[1]}.json"
source = PointSetTriangulationParser.parse(source_file)
target_file = f"{sys.argv[2]}.json"
target = PointSetTriangulationParser.parse(target_file)
shortest_sequence = exhaustive_simultanious_flip_graph_search(source, target)
shortest_sequence_ignore_happy = exhaustive_simultanious_flip_graph_search(source, target, ignore_happy_edges=True)

print(f"flippable edges: {source.get_flippable_edges()}")
print(f"independent flip sets : {source.get_independent_flip_sets()}")
print("shortest flip sequence to target:")
if shortest_sequence is not None:
  for i, step_data in enumerate(shortest_sequence):
    print(f"Step {i+1}: Flip edges {step_data.flip_set} (maximum set: {step_data.maximum_set})")
print("shortest flip sequence to target (ignoring happy edges):")
if shortest_sequence_ignore_happy is not None:
  for i, step_data in enumerate(shortest_sequence_ignore_happy):
    print(f"Step {i+1}: Flip edges {step_data.flip_set} (maximum set: {step_data.maximum_set})")