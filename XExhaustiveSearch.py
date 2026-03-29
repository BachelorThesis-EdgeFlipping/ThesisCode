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
  print("Usage: python XExhaustiveSearch.py <parser_type> <run_suite> <source/suite> <target>")
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
  if len(sys.argv) != 5:
    error_incorrect_arguments()
  source_names = [sys.argv[3]]
  target_names = [sys.argv[4]]
  sources = [parser.parse(f"{data_folder}{sys.argv[3]}.json")]
  targets = [parser.parse(f"{data_folder}{sys.argv[4]}.json")]
if sys.argv[2] == "-suite":
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
print(f"\rProgress: calculated problem pairs 0/{total_problem_pairs}", end="", flush=True)
for pair_index, (source, target) in enumerate(zip(sources, targets), start=1):
  source_label = source_names[pair_index - 1] if pair_index - 1 < len(source_names) else str(pair_index)
  target_label = target_names[pair_index - 1] if pair_index - 1 < len(target_names) else str(pair_index)
  result, timed_out = exhaustive_simultanious_flip_graph_search(source, target, ignore_happy_edges=True, timeout=600)
  shortest_sequence_ignore_happy.append((result, timed_out))
  timed_out_pairs.append(timed_out)
  print(f"\rProgress: calculated problem pairs {pair_index}/{total_problem_pairs} ({source_label} -> {target_label})", end="", flush=True)
print()
timer_end_search_overall = time.time()

#####################
#  results output   #
#####################
print()
print("###### Results ######")
print()

for index, (result, timed_out) in enumerate(shortest_sequence_ignore_happy):
  print(f"--- Problem {index+1}: {source_names[index]} -> {target_names[index]} ---")
  if timed_out:
    print(f"TIMEOUT: Search exceeded 10-minute limit.")
  elif result is not None:
    print(f"Found {len(result)} optimal path(s) of length {len(result[0])}:")
    for j, sequence in enumerate(result):
      print(f"  Path {j+1}:")
      for i, step_data in enumerate(sequence):
        print(f"    {i+1}: {step_data.flip_set} (maximal set: {str(step_data.maximal_set).upper()})")
    has_non_maximal_path = any(any(not step.maximal_set for step in path) for path in result)
    print(f"Optimal path with at least one non-maximal set exists: {str(has_non_maximal_path).upper()}")
    print_edge_set_groups(result)
  else:
    print("No path found.")
  print()

twin_status_counts = {"ONE": 0, "BOTH": 0, "NONE": 0}
twin_pairs_total = 0

if is_suite:
  print("###### Suite Overview ######")
  print()
  count_with_maximal_path = 0
  count_solved = 0
  count_timed_out = sum(1 for t in timed_out_pairs if t)
  problem_has_all_maximal_path: list[bool] = []
  tested_directed_pairs: set[tuple[str, str]] = set()
  for index, (result, timed_out) in enumerate(shortest_sequence_ignore_happy):
    tested_directed_pairs.add((source_names[index], target_names[index]))
    has_all_maximal_path = False
    if timed_out:
      problem_has_all_maximal_path.append(False)
      print(f"  Problem {index+1}: {source_names[index]} -> {target_names[index]} | TIMED OUT")
    elif result is not None:
      count_solved += 1
      has_all_maximal_path = has_optimal_all_maximal_path(result)
      if has_all_maximal_path:
        count_with_maximal_path += 1
      problem_has_all_maximal_path.append(has_all_maximal_path)
      num_classes = len(get_edge_set_groups(result))
      status = str(has_all_maximal_path).upper()
      print(f"  Problem {index+1}: {source_names[index]} -> {target_names[index]} | paths: {len(result)} | eq. classes: {num_classes} | all-maximal optimal path: {status}")
    else:
      problem_has_all_maximal_path.append(False)
      print(f"  Problem {index+1}: {source_names[index]} -> {target_names[index]} | no path found")
  print()
  total = len(shortest_sequence_ignore_happy)
  pct_solved = convert_to_pct(count_with_maximal_path, count_solved)
  print()

  print("###### Twin Pair Overview ######")
  print()
  twin_map: dict[tuple[str, str], dict[str, tuple[bool, bool]]] = {}
  for index, result in enumerate(shortest_sequence_ignore_happy):
    source_name = source_names[index]
    target_name = target_names[index]
    if source_name == target_name:
      continue
    key = (min(source_name, target_name), max(source_name, target_name))
    direction = f"{source_name}->{target_name}"
    if key not in twin_map:
      twin_map[key] = {}
    # (has_all_maximal_path, timed_out)
    twin_map[key][direction] = (problem_has_all_maximal_path[index], timed_out_pairs[index])
  sorted_twin_items = sorted(twin_map.items())
  for (name_a, name_b), directional_results in sorted_twin_items:
    forward_key = f"{name_a}->{name_b}"
    backward_key = f"{name_b}->{name_a}"
    if forward_key not in directional_results or backward_key not in directional_results:
      continue
    forward_has, forward_timed_out = directional_results[forward_key]
    backward_has, backward_timed_out = directional_results[backward_key]
    if forward_timed_out or backward_timed_out:
      continue
    if forward_has and backward_has:
      twin_status = "BOTH"
    elif forward_has or backward_has:
      twin_status = "ONE"
    else:
      twin_status = "NONE"
    twin_status_counts[twin_status] += 1
    twin_pairs_total += 1
    print(f"Twin problem pair ({name_a} <-> {name_b}): {twin_status}")
  one_pairs = [(name_a, name_b) for (name_a, name_b), directional_results in sorted_twin_items
    if f"{name_a}->{name_b}" in directional_results and f"{name_b}->{name_a}" in directional_results
    and (not directional_results[f"{name_a}->{name_b}"][1])
    and (not directional_results[f"{name_b}->{name_a}"][1])
    and (directional_results[f"{name_a}->{name_b}"][0] != directional_results[f"{name_b}->{name_a}"][0])]
  if one_pairs:
    print(f"Twin pairs where only ONE direction has an all-maximal optimal path ({len(one_pairs)}):")
    for name_a, name_b in one_pairs:
      forward_has = twin_map[(name_a, name_b)][f"{name_a}->{name_b}"][0]
      direction = f"{name_a}->{name_b}" if forward_has else f"{name_b}->{name_a}"
      print(f"  ({name_a} <-> {name_b}): {direction} has all-maximal optimal path")
    print()
  
  #calculate statistics
  solved_twin_pairs_pct = convert_to_pct(twin_pairs_total, count_solved)
  twin_one_pct = convert_to_pct(twin_status_counts["ONE"], twin_pairs_total)
  twin_both_pct = convert_to_pct(twin_status_counts["BOTH"], twin_pairs_total)
  twin_none_pct = convert_to_pct(twin_status_counts["NONE"], twin_pairs_total)

  unique_triangulations = len(set(source_names + target_names))
  possible_directed_pairs = unique_triangulations * (unique_triangulations - 1)
  tested_directed_pairs_count = len([1 for s, t in tested_directed_pairs if s != t])
  tested_directed_pct = convert_to_pct(tested_directed_pairs_count, possible_directed_pairs)
  has_consistent_order = False
  consistent_order = None
  if convex_polygon_realm:
    has_consistent_order, consistent_order = all_triangulations_have_same_order(sources + targets)
  if has_consistent_order and consistent_order is not None:
    possible_overall_triangulations = number_possible_triangulations(consistent_order)
    tested_overall_triangulations_pct = convert_to_pct(unique_triangulations, possible_overall_triangulations)
    possible_overall_directed_pairs = number_possible_ordered_pairs(consistent_order)
    tested_overall_directed_pct = convert_to_pct(tested_directed_pairs_count, possible_overall_directed_pairs)

  print()
  print("###### Statistics ######")
  print(f"Problems solved: {count_solved}/{total}")
  print(f"Problems timed out: {count_timed_out}/{total}")
  print(f"Solved problems with at least one all-maximal path: {count_with_maximal_path}/{count_solved} solved ({pct_solved:.1f}%)")
  print(f"Tested ordered pairs over the possible pairs for given triangulations: {tested_directed_pairs_count}/{possible_directed_pairs} ({tested_directed_pct:.1f}%)")
  if has_consistent_order and consistent_order is not None:
    print(f"Involved distinct triangulations over all possible triangulations for order n={consistent_order}: {unique_triangulations}/{possible_overall_triangulations} ({tested_overall_triangulations_pct:.1f}%)")
    print(f"Tested ordered pairs over all possible pairs for order n={consistent_order}: {tested_directed_pairs_count}/{possible_overall_directed_pairs} ({tested_overall_directed_pct:.1f}%)")
  print(f"Number of (solved) problems with a twin problem: {twin_pairs_total*2}/{count_solved} ({solved_twin_pairs_pct*2:.1f}%)")
  print(f"Twin pair distribution (all-maximal path): ONE {twin_one_pct:.1f}% | BOTH {twin_both_pct:.1f}% | NONE {twin_none_pct:.1f}%")
  print()

print("###### Runtime ######")
print(f"  Parsing: {timer_end_parsing - timer_start_parsing:.4f}s")
print(f"  Search:  {timer_end_search_overall - timer_start_search_overall:.4f}s")
print(f"  Total:   {timer_end_search_overall - timer_start_parsing:.4f}s")
  

