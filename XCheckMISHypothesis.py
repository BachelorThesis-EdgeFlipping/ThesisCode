from datetime import datetime
import os
import sys
import time
from data_structures.Triangulation import Triangulation
from Models import Edge, ImportSuite
from io_utils.PointSetTriangulationParser import PointSetTriangulationParser
from io_utils.ConvexPolygonTriangulationParser import ConvexPolygonTriangulationParser
from io_utils.Parser import Parser
from ExhaustiveSearchAlgorithm import StepData, exhaustive_simultanious_flip_graph_search
from math import comb

##################
#     helpers    #
##################

#calculate number of possible directed pairs of triangulations for a given order n (ignoring diagonal pairs)
def number_possible_triangulations(order: int) -> int:
  if order < 3:
    return 0
  return comb(2*(order-2), (order-2)) // (order-1)

def number_possible_ordered_pairs(order: int) -> int:
  possible_triangulations = number_possible_triangulations(order)
  return possible_triangulations * (possible_triangulations - 1)

def get_vertex_set_key(triangulation: Triangulation) -> tuple[tuple[float, float], ...]:
  return tuple(sorted((vertex.x, vertex.y) for vertex in triangulation.vertices))

def number_possible_ordered_pairs_by_vertex_set(triangulations: list[Triangulation]) -> int:
  grouped_counts: dict[tuple[tuple[float, float], ...], int] = {}
  for triangulation in triangulations:
    key = get_vertex_set_key(triangulation)
    grouped_counts[key] = grouped_counts.get(key, 0) + 1
  return sum(count * (count - 1) for count in grouped_counts.values())

def all_triangulations_have_same_order(triangulations: list[Triangulation]) -> tuple[bool, int | None]:
  if not triangulations:
    return (False, None)
  orders = {len(tri.vertices) for tri in triangulations}
  if len(orders) != 1:
    return (False, None)
  return (True, next(iter(orders)))

def convert_to_pct(count: int, total: int) -> float:
  return (count / total * 100) if total > 0 else 0

def get_path_edge_set(path: list[StepData]) -> frozenset[Edge]:
  edges = set()
  for step in path:
    for e in step.flip_set:
      edges.add((min(e[0], e[1]), max(e[0], e[1])))
  return frozenset(edges)

def get_edge_set_groups(paths: list[list[StepData]]) -> dict[frozenset[Edge], list[int]]:
  groups: dict[frozenset[Edge], list[int]] = {}
  for index, path in enumerate(paths):
    key = get_path_edge_set(path)
    groups.setdefault(key, []).append(index + 1)
  return groups

def has_optimal_all_maximal_path(paths: list[list[StepData]] | None) -> bool:
  if paths is None:
    return False
  return any(all(step.maximal_set for step in path) for path in paths)

##################
# output helpers #
##################
def error_incorrect_arguments():
  print("Usage: python XExhaustiveSearch.py <parser_type> <run_suite> <source/suite> <target> <optional: -log")
  print("  parser_type: -ps = PointSetTriangulationParser, -cp = ConvexPolygonTriangulationParser")
  print("  run_suite: -suite = run all problem pairs from suite, -no_suite = run problem single pair")
  sys.exit(1)


def print_edge_set_groups(paths: list[list[StepData]]):
  groups = get_edge_set_groups(paths)
  print(f"  {len(groups)} equivalence class(es) by total edge set:")
  for i, (edge_set, path_indices) in enumerate(groups.items(), 1):
    has_all_maximal = any(
      all(step.maximal_set for step in paths[idx - 1])
      for idx in path_indices
    )
    print(f"  Class {i}. (contains all-maximal path: {str(has_all_maximal).upper()})")
    print(f"    - Paths {path_indices}")
    print(f"    - edges flipped {sorted(edge_set)}")

def print_and_log_progress(progress_message: str):
  #if printing not (only) to console, ensure progress messages are flushed immediately
  if not sys.stdout.isatty():
    print(progress_message, flush=True)
  #if only printing to console, overwrite the same line for singe line progress updates
  else:
    print(f"\r{progress_message:<80}", end="", flush=True)
  if log_progress:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"[{now}] {progress_message}\n")
    #immediate flush to ensure log is up to date even if program is interrupted (useful for freezes)
    log_file.flush()
    os.fsync(log_file.fileno())


############
#   main   #
############

parser: Parser
data_folder: str
sources: list[Triangulation]
targets: list[Triangulation]
source_names: list[str] = []
target_names: list[str] = []
is_suite: bool = False
convex_polygon_realm = False
log_file = open("test_results/logs/progress.log", "a")
log_progress = False

#program arguments
timer_start_parsing = time.time()
if len(sys.argv) < 4:
  error_incorrect_arguments()
if sys.argv[1] == "-cp":
  parser = ConvexPolygonTriangulationParser
  data_folder = "convex_polygon/"
  convex_polygon_realm = True
elif sys.argv[1] == "-ps":
  parser = PointSetTriangulationParser
  data_folder = "point_set/"
else:
  error_incorrect_arguments()
if sys.argv[2] == "-no_suite":
  if(len(sys.argv) > 5):
    error_incorrect_arguments()
  source_names = [sys.argv[3]]
  target_names = [sys.argv[4]]
  sources = [parser.parse(f"{data_folder}{sys.argv[3]}.json")]
  targets = [parser.parse(f"{data_folder}{sys.argv[4]}.json")]

if sys.argv[2] == "-suite":
  if(len(sys.argv) > 5):
    error_incorrect_arguments()
  if(len(sys.argv) == 5):
    if sys.argv[4] != "-log":
      error_incorrect_arguments()  
    log_progress = True
  is_suite = True
  suite_file = f"suites/{sys.argv[3]}.json"
  suite = ImportSuite.from_json(Parser.getJSONString(suite_file))
  path_prefix = suite.path_prefix if suite.path_prefix else ""
  if(len(suite.sources) != len(suite.targets)):
    print("Error: number of sources and targets in suite must match.")
    sys.exit(1)
  source_names = suite.sources
  target_names = suite.targets
  sources = [parser.parse(f"{data_folder}{path_prefix}{name}.json") for name in suite.sources]
  targets = [parser.parse(f"{data_folder}{path_prefix}{name}.json") for name in suite.targets]
timer_end_parsing = time.time()

#####################################
#  run exhaustive search algorithm  #
#####################################

timer_start_search_overall = time.time()
total_problem_pairs = len(sources)
shortest_sequence_ignore_happy: list[tuple[list[list[StepData]] | None, bool]] = []
timed_out_pairs: list[bool] = []
for pair_index, (source, target) in enumerate(zip(sources, targets), start=1):
  source_label = source_names[pair_index - 1] if pair_index - 1 < len(source_names) else str(pair_index)
  target_label = target_names[pair_index - 1] if pair_index - 1 < len(target_names) else str(pair_index)
  
  try:
    result, timed_out = exhaustive_simultanious_flip_graph_search(
        source, 
        target, 
        ignore_happy_edges=True, 
        only_flip_maximal_sets=True, 
        only_flip_descreasing_intersection_score=True, 
        only_one_path_per_state=True, 
        timeout=600
    )
  except ValueError as e:
    print_and_log_progress(f"Skipping pair {pair_index}/{total_problem_pairs} ({source_label} -> {target_label}). Reason: Incompatible point sets.")
    shortest_sequence_ignore_happy.append((None, False))
    timed_out_pairs.append(False)
    continue

  shortest_sequence_ignore_happy.append((result, timed_out))
  timed_out_pairs.append(timed_out)
  timeout_suffix = " | TIMED OUT" if timed_out else ""
  print_and_log_progress(f"Progress: calculated problem pairs {pair_index}/{total_problem_pairs} ({source_label} -> {target_label}){timeout_suffix}")
  
  if not timed_out and (result is None or len(result) == 0):
    print(f"\n\nBREAK: No path found for instance {source_label} -> {target_label}. Terminating early.")
    sys.exit(1)
print()
timer_end_search_overall = time.time()
log_file.close()

#####################
#  results output   #
#####################
print()
print("###### Results ######")
print()

success_count = 0
timeout_count = sum(1 for t in timed_out_pairs if t)
failed_count = 0

print("###### Paths Found ######")
for index, (result, timed_out) in enumerate(shortest_sequence_ignore_happy):
  if timed_out:
    pass
  elif result is not None and len(result) > 0:
    success_count += 1
    source_label = source_names[index] if index < len(source_names) else str(index + 1)
    target_label = target_names[index] if index < len(target_names) else str(index + 1)
    print(f"Path for {source_label} -> {target_label}:")
    for step_idx, step in enumerate(result[0], 1):
      edges_str = sorted([(min(e), max(e)) for e in step.flip_set])
      print(f"  Step {step_idx}: diff {step.intersection_diff}, flips {edges_str}")
  else:
    failed_count += 1

total = len(shortest_sequence_ignore_happy)

print(f"Total Problem Pairs: {total}")
print(f"Paths Found: {success_count}")
print(f"No Path Found: {failed_count}")
print(f"Timeouts: {timeout_count}")
print()

print()
print("###### Runtime ######")
print(f"  Parsing: {timer_end_parsing - timer_start_parsing:.4f}s")
print(f"  Search:  {timer_end_search_overall - timer_start_search_overall:.4f}s")
print(f"  Total:   {timer_end_search_overall - timer_start_parsing:.4f}s")
