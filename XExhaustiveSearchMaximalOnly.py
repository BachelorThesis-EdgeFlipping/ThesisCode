import sys
import time
from data_structures.Triangulation import Triangulation
from Models import ImportSuite
from io_utils.PointSetTriangulationParser import PointSetTriangulationParser
from io_utils.ConvexPolygonTriangulationParser import ConvexPolygonTriangulationParser
from io_utils.Parser import Parser
from ExhaustiveSearchAlgorithm import exhaustive_simultanious_flip_graph_search

##################
#   helpers      #
##################

def calculate_intersection_score(tri1: Triangulation, tri2: Triangulation) -> int:
  return tri1.count_geometric_crossings_with(tri2)

def get_path_score_progression(source: Triangulation, target: Triangulation, path):
	tmp = source.deep_copy()
	step_scores: list[tuple[int, int, int]] = []
	start_score = calculate_intersection_score(tmp, target)
	before_score = start_score
	for step in path:
		tmp.flip_edges_simultaneous(step.flip_set)
		after_score = calculate_intersection_score(tmp, target)
		step_scores.append((before_score, after_score, after_score - before_score))
		before_score = after_score
	return start_score, before_score, step_scores

##################
# output helpers #
##################
def error_incorrect_arguments():
	print("Usage: python XExhaustiveSearchMaximalOnly.py <parser_type> <run_suite> <source/suite> <target>")
	print("  run_suite: -suite = run all problem pairs from suite, -no_suite = run problem single pair")
	print("  parser_type: -ps = PointSetTriangulationParser, -cp = ConvexPolygonTriangulationParser")
	sys.exit(1)


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

# program arguments
timer_start_parsing = time.time()
if len(sys.argv) < 4:
	error_incorrect_arguments()
if sys.argv[1] == "-cp":
	parser = ConvexPolygonTriangulationParser
	data_folder = "convex_polygon/"
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
	if len(suite.sources) != len(suite.targets):
		print("Error: number of sources and targets in suite must match.")
		sys.exit(1)
	source_names = suite.sources
	target_names = suite.targets
	sources = [parser.parse(f"{data_folder}{path_prefix}{name}.json") for name in suite.sources]
	targets = [parser.parse(f"{data_folder}{path_prefix}{name}.json") for name in suite.targets]
if sys.argv[2] not in ("-suite", "-no_suite"):
	error_incorrect_arguments()
timer_end_parsing = time.time()


#################################################
# run exhaustive  maximal-only search algorithm #
#################################################

timer_start_search_overall = time.time()
total_problem_pairs = len(sources)
search_results: list[tuple[list[list] | None, bool]] = []

print(f"\rProgress: calculated problem pairs 0/{total_problem_pairs}", end="", flush=True)
for pair_index, (source, target) in enumerate(zip(sources, targets), start=1):
	source_label = source_names[pair_index - 1] if pair_index - 1 < len(source_names) else str(pair_index)
	target_label = target_names[pair_index - 1] if pair_index - 1 < len(target_names) else str(pair_index)
	result, timed_out = exhaustive_simultanious_flip_graph_search(
		source,
		target,
		ignore_happy_edges=True,
		only_flip_maximal_sets=True,
		only_flip_descreasing_intersection_score=True,
		never_flip_positive_intersection_score_flips=True,
		only_one_path_per_state=True,
	)
	search_results.append((result, timed_out))
	print(
		f"\rProgress: calculated problem pairs {pair_index}/{total_problem_pairs} ({source_label} -> {target_label})",
		end="",
		flush=True
	)
print()
timer_end_search_overall = time.time()


#####################
#  results output   #
#####################
print()
print("###### Maximal-Only Path Existence Results ######")
print()

exists_count = 0
timeout_count = 0

for index, (result, timed_out) in enumerate(search_results):
	source_name = source_names[index] if index < len(source_names) else str(index + 1)
	target_name = target_names[index] if index < len(target_names) else str(index + 1)
	print(f"--- Problem {index + 1}: {source_name} -> {target_name} ---")
	if timed_out:
		timeout_count += 1
		print("TIMED OUT: Search exceeded 10-minute limit.")
	elif result is not None:
		exists_count += 1
		print("PATH EXISTS (maximal-flip-only): TRUE")
		print(f"Shortest maximal-only path length: {len(result[0])}")
		for path_index, path in enumerate(result, start=1):
			start_score, end_score, step_scores = get_path_score_progression(sources[index], targets[index], path)
			net_diff = end_score - start_score
			print(f"  Path {path_index}:")
			print(f"    Net intersection-score diff (crossings): {start_score} -> {end_score} (delta {net_diff:+d})")
			if not path:
				print("    No flips needed.")
			for step_index, step in enumerate(path, start=1):
				before_score, after_score, step_diff = step_scores[step_index - 1]
				print(f"    {step_index}: flips={step.flip_set} | score {before_score} -> {after_score} (delta {step_diff:+d})")
	else:
		print("PATH EXISTS (maximal-flip-only): FALSE")
	print()

if is_suite:
	total = len(search_results)
	solved_count = total - timeout_count
	print("###### Suite Overview ######")
	print()
	print(f"Total problems: {total}")
	print(f"Timed out: {timeout_count}/{total}")
	print(f"Solved (finished search): {solved_count}/{total}")
	if solved_count > 0:
		print(f"With maximal-only & intersection decreasing path existing: {exists_count}/{solved_count}")
	else:
		print("With maximal-only & intersection decreasing path existing: 0/0")
	print()

print("###### Runtime ######")
print(f"  Parsing: {timer_end_parsing - timer_start_parsing:.4f}s")
print(f"  Search:  {timer_end_search_overall - timer_start_search_overall:.4f}s")
print(f"  Total:   {timer_end_search_overall - timer_start_parsing:.4f}s")
