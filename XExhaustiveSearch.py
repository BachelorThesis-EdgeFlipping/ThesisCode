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
  target: Triangulation
) -> list[list[Edge]] | None:
  if source == target:
    return []
  #BFS: each entry is a SearchState
  #visited for caching triangulation hashes to avoid revisiting
  visited: set[int] = {hash(source)}
  queue: deque[SearchState] = deque()
  queue.append(SearchState(source, []))
  while queue:
    current_node = queue.popleft()
    current_tri, path = current_node.tri, current_node.path
    flip_sets = current_tri.get_independent_flip_sets()
    for flip_set in flip_sets:
      neighbor = current_tri.deep_copy()
      neighbor.flip_edges_simultaneous(flip_set)
      if neighbor == target:
        return path + [StepData(flip_set, True)]
      h = hash(neighbor)
      if h not in visited:
        visited.add(h)
        queue.append(SearchState(neighbor, path + [StepData(flip_set, False)]))
  return None

############
#   main   #
############
source_file = f"{sys.argv[1]}.json"
source = PointSetTriangulationParser.parse(source_file)
target_file = f"{sys.argv[2]}.json"
target = PointSetTriangulationParser.parse(target_file)
shortest_sequence = exhaustive_simultanious_flip_graph_search(source, target)

print(f"flippable edges: {source.get_flippable_edges()}")
print(f"independent flip sets : {source.get_independent_flip_sets()}")
print("shortest flip sequence to target:")
if shortest_sequence is not None:
  for i, step_data in enumerate(shortest_sequence):
    print(f"Step {i+1}: Flip edges {step_data.flip_set} (maximum set: {step_data.maximum_set})")