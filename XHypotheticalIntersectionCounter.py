import sys
import time

from data_structures.Triangulation import Triangulation
from Models import Edge, ImportSuite
from io_utils.PointSetTriangulationParser import PointSetTriangulationParser
from io_utils.ConvexPolygonTriangulationParser import ConvexPolygonTriangulationParser
from io_utils.Parser import Parser


##################
#   helpers      #
##################

def error_incorrect_arguments():
	print("Usage: python XHypotheticalIntersectionCounter.py <parser_type> <run_suite> <source/suite> <target>")
	print("  parser_type: -ps = PointSetTriangulationParser, -cp = ConvexPolygonTriangulationParser")
	print("  run_suite: -suite = run all problem pairs from suite, -no_suite = run single problem pair")
	sys.exit(1)


def normalize_edge(edge: Edge) -> Edge:
	return (min(edge[0], edge[1]), max(edge[0], edge[1]))


def convert_to_pct(count: int, total: int) -> float:
	return (count / total * 100) if total > 0 else 0.0


def is_flippable_edge_graph_two_colorable(tri: Triangulation, flippable_edges: list[Edge]) -> bool:
	# Build graph only from flippable edges.
	adjacency: dict[int, set[int]] = {}
	for a, b in flippable_edges:
		if a not in adjacency:
			adjacency[a] = set()
		if b not in adjacency:
			adjacency[b] = set()
		adjacency[a].add(b)
		adjacency[b].add(a)

	color: dict[int, int] = {}
	for start in adjacency:
		if start in color:
			continue
		color[start] = 0
		stack = [start]
		while stack:
			u = stack.pop()
			for v in adjacency[u]:
				if v not in color:
					color[v] = 1 - color[u]
					stack.append(v)
				elif color[v] == color[u]:
					return False
	return True


def compute_edge_differences(source: Triangulation, target: Triangulation) -> tuple[int, list[tuple[Edge, int, int, int]], int, bool, int, bool]:
	"""
	Returns:
		baseline_score,
		per_edge_results: [(edge, before, after, delta_after_minus_before)],
		total_delta_sum,
		has_happy_flippable_edge,
		number_of_happy_flippable_edges,
		flippable_edge_graph_is_two_colorable
	"""
	baseline_score = source.count_geometric_crossings_with(target)
	flippable_edges = source.get_flippable_edges()
	target_edges = target.edge_set()
	flippable_edge_graph_is_two_colorable = is_flippable_edge_graph_two_colorable(source, flippable_edges)

	happy_flippable_edges = [e for e in flippable_edges if normalize_edge(e) in target_edges]
	has_happy_flippable_edge = len(happy_flippable_edges) > 0

	per_edge_results: list[tuple[Edge, int, int, int]] = []
	total_delta_sum = 0
	for edge in flippable_edges:
		tri_after_flip = source.deep_copy()
		can_flip = tri_after_flip.flip_edge(edge[0], edge[1])
		if not can_flip:
			raise Exception(f"Edge {edge} was listed as flippable but could not be flipped.")
		after_score = tri_after_flip.count_geometric_crossings_with(target)
		delta = after_score - baseline_score
		per_edge_results.append((edge, baseline_score, after_score, delta))
		total_delta_sum += delta

	return baseline_score, per_edge_results, total_delta_sum, has_happy_flippable_edge, len(happy_flippable_edges), flippable_edge_graph_is_two_colorable


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
elif sys.argv[2] == "-suite":
	if len(sys.argv) != 4:
		error_incorrect_arguments()
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
else:
	error_incorrect_arguments()

timer_end_parsing = time.time()


###############################################
# run hypothetical single-edge flip analysis  #
###############################################

timer_start_analysis = time.time()
total_problem_pairs = len(sources)

# (baseline, per_edge_results, total_delta_sum, has_happy_edge, happy_edge_count, flippable_edge_graph_is_two_colorable)
analysis_results: list[tuple[int, list[tuple[Edge, int, int, int]], int, bool, int, bool]] = []

print(f"\rProgress: analyzed problem pairs 0/{total_problem_pairs}", end="", flush=True)
for pair_index, (source, target) in enumerate(zip(sources, targets), start=1):
	source_label = source_names[pair_index - 1] if pair_index - 1 < len(source_names) else str(pair_index)
	target_label = target_names[pair_index - 1] if pair_index - 1 < len(target_names) else str(pair_index)
	analysis_results.append(compute_edge_differences(source, target))
	print(
		f"\rProgress: analyzed problem pairs {pair_index}/{total_problem_pairs} ({source_label} -> {target_label})",
		end="",
		flush=True,
	)
print()

timer_end_analysis = time.time()


####################
# detailed output  #
####################

print()
print("###### Hypothetical Intersection Difference Results ######")
print()

pair_total_negative_count = 0
pair_total_zero_count = 0
pair_total_positive_count = 0
pair_total_non_positive_count = 0

for index, (baseline_score, per_edge_results, total_delta_sum, has_happy_edge, happy_edge_count, flippable_edge_graph_is_two_colorable) in enumerate(analysis_results):
	source_name = source_names[index] if index < len(source_names) else str(index + 1)
	target_name = target_names[index] if index < len(target_names) else str(index + 1)

	if total_delta_sum < 0:
		pair_total_negative_count += 1
	elif total_delta_sum > 0:
		pair_total_positive_count += 1
	else:
		pair_total_zero_count += 1
	if total_delta_sum <= 0:
		pair_total_non_positive_count += 1

	print(f"--- Problem {index + 1}: {source_name} -> {target_name} ---")
	print(f"Baseline intersection score: {baseline_score}")
	print(f"Flippable edges in A: {len(per_edge_results)}")
	print(f"A has happy flippable edge(s): {str(has_happy_edge).upper()} (count: {happy_edge_count})")
	print(f"Flippable-edge graph in A is 2-colorable: {str(flippable_edge_graph_is_two_colorable).upper()}")

	negative_edge_deltas = sum(1 for _, _, _, delta in per_edge_results if delta < 0)
	positive_edge_deltas = sum(1 for _, _, _, delta in per_edge_results if delta > 0)
	zero_edge_deltas = len(per_edge_results) - negative_edge_deltas - positive_edge_deltas
	print(
		"Edge delta distribution: "
		f"negative {negative_edge_deltas}, zero {zero_edge_deltas}, positive {positive_edge_deltas}"
	)

	print(f"Sum of all individual edge deltas (flipped - not_flipped): {total_delta_sum:+d}")
	if total_delta_sum < 0:
		print("Pair total intersection difference score < 0: TRUE")
	else:
		print("Pair total intersection difference score < 0: FALSE")

	if per_edge_results:
		print("Per-edge deltas:")
		for edge, before_score, after_score, delta in per_edge_results:
			print(f"  edge {edge}: {before_score} -> {after_score} (delta {delta:+d})")
	else:
		print("Per-edge deltas: no flippable edges in A")
	print()


##################
# suite overview #
##################

print("###### Overview ######")
print()
total_pairs = len(analysis_results)
negative_pct = convert_to_pct(pair_total_negative_count, total_pairs)
non_positive_pct = convert_to_pct(pair_total_non_positive_count, total_pairs)
print(f"Problem pairs with total intersection difference score < 0: {pair_total_negative_count}/{total_pairs} ({negative_pct:.1f}%)")
print(f"Problem pairs with total intersection difference score <= 0: {pair_total_non_positive_count}/{total_pairs} ({non_positive_pct:.1f}%)")
print(
	"Pair total sign distribution: "
	f"negative {pair_total_negative_count}, "
	f"zero {pair_total_zero_count}, "
	f"positive {pair_total_positive_count}"
)

# grouped by happy-edge existence
group_stats = {
	True: {"pairs": 0, "neg_pairs": 0, "non_pos_pairs": 0, "sum_total_delta": 0, "sum_happy_edges": 0},
	False: {"pairs": 0, "neg_pairs": 0, "non_pos_pairs": 0, "sum_total_delta": 0, "sum_happy_edges": 0},
}

for _, _, total_delta_sum, has_happy_edge, happy_edge_count, _ in analysis_results:
	group_stats[has_happy_edge]["pairs"] += 1
	if total_delta_sum < 0:
		group_stats[has_happy_edge]["neg_pairs"] += 1
	if total_delta_sum <= 0:
		group_stats[has_happy_edge]["non_pos_pairs"] += 1
	group_stats[has_happy_edge]["sum_total_delta"] += total_delta_sum
	group_stats[has_happy_edge]["sum_happy_edges"] += happy_edge_count

two_color_group_stats = {
	True: {"pairs": 0, "neg_pairs": 0, "non_pos_pairs": 0, "sum_total_delta": 0},
	False: {"pairs": 0, "neg_pairs": 0, "non_pos_pairs": 0, "sum_total_delta": 0},
}

for _, _, total_delta_sum, _, _, flippable_edge_graph_is_two_colorable in analysis_results:
	two_color_group_stats[flippable_edge_graph_is_two_colorable]["pairs"] += 1
	if total_delta_sum < 0:
		two_color_group_stats[flippable_edge_graph_is_two_colorable]["neg_pairs"] += 1
	if total_delta_sum <= 0:
		two_color_group_stats[flippable_edge_graph_is_two_colorable]["non_pos_pairs"] += 1
	two_color_group_stats[flippable_edge_graph_is_two_colorable]["sum_total_delta"] += total_delta_sum

combined_two_col_no_happy_pairs = 0
combined_two_col_no_happy_neg_pairs = 0
combined_two_col_no_happy_non_pos_pairs = 0
for _, _, total_delta_sum, has_happy_edge, _, flippable_edge_graph_is_two_colorable in analysis_results:
	if flippable_edge_graph_is_two_colorable and not has_happy_edge:
		combined_two_col_no_happy_pairs += 1
		if total_delta_sum < 0:
			combined_two_col_no_happy_neg_pairs += 1
		if total_delta_sum <= 0:
			combined_two_col_no_happy_non_pos_pairs += 1

combined_two_col_no_happy_pct = convert_to_pct(combined_two_col_no_happy_pairs, total_pairs)
combined_two_col_no_happy_neg_pct = convert_to_pct(combined_two_col_no_happy_neg_pairs, combined_two_col_no_happy_pairs)
combined_two_col_no_happy_non_pos_pct = convert_to_pct(combined_two_col_no_happy_non_pos_pairs, combined_two_col_no_happy_pairs)

print()
print("By happy-edge existence in A:")
for has_happy_edge in (True, False):
	label = "HAPPY EDGE EXISTS" if has_happy_edge else "NO HAPPY EDGE"
	pairs = group_stats[has_happy_edge]["pairs"]
	neg_pairs = group_stats[has_happy_edge]["neg_pairs"]
	non_pos_pairs = group_stats[has_happy_edge]["non_pos_pairs"]
	sum_total_delta = group_stats[has_happy_edge]["sum_total_delta"]
	sum_happy_edges = group_stats[has_happy_edge]["sum_happy_edges"]
	neg_pct_group = convert_to_pct(neg_pairs, pairs)
	non_pos_pct_group = convert_to_pct(non_pos_pairs, pairs)
	avg_total_delta = (sum_total_delta / pairs) if pairs > 0 else 0.0
	avg_happy_edges = (sum_happy_edges / pairs) if pairs > 0 else 0.0

	print(f"  {label}:")
	print(f"    Pairs: {pairs}")
	print(f"    Pairs with total score < 0: {neg_pairs}/{pairs} ({neg_pct_group:.1f}%)")
	print(f"    Pairs with total score <= 0: {non_pos_pairs}/{pairs} ({non_pos_pct_group:.1f}%)")
	print(f"    Average summed delta score: {avg_total_delta:.3f}")
	print(f"    Average number of happy flippable edges in A: {avg_happy_edges:.3f}")

no_happy_pairs = group_stats[False]["pairs"]
no_happy_non_pos_pairs = group_stats[False]["non_pos_pairs"]
no_happy_non_pos_pct = convert_to_pct(no_happy_non_pos_pairs, no_happy_pairs)
print()
print(
	f"Metric (NO HAPPY EDGE only) with total score <= 0: "
	f"{no_happy_non_pos_pairs}/{no_happy_pairs} ({no_happy_non_pos_pct:.1f}%)"
)

print()
print("By flippable-edge graph 2-colorability in A:")
for is_two_col in (True, False):
	label = "FLIPPABLE-EDGE GRAPH IS 2-COLORABLE" if is_two_col else "FLIPPABLE-EDGE GRAPH IS NOT 2-COLORABLE"
	pairs = two_color_group_stats[is_two_col]["pairs"]
	neg_pairs = two_color_group_stats[is_two_col]["neg_pairs"]
	non_pos_pairs = two_color_group_stats[is_two_col]["non_pos_pairs"]
	sum_total_delta = two_color_group_stats[is_two_col]["sum_total_delta"]
	neg_pct_group = convert_to_pct(neg_pairs, pairs)
	non_pos_pct_group = convert_to_pct(non_pos_pairs, pairs)
	avg_total_delta = (sum_total_delta / pairs) if pairs > 0 else 0.0

	print(f"  {label}:")
	print(f"    Pairs: {pairs}")
	print(f"    Pairs with total score < 0: {neg_pairs}/{pairs} ({neg_pct_group:.1f}%)")
	print(f"    Pairs with total score <= 0: {non_pos_pairs}/{pairs} ({non_pos_pct_group:.1f}%)")
	print(f"    Average summed delta score: {avg_total_delta:.3f}")

print()
print("Combined condition: 2-colorable + no happy edges")
print(
	f"  Pairs matching condition: {combined_two_col_no_happy_pairs}/{total_pairs} "
	f"({combined_two_col_no_happy_pct:.1f}%)"
)
print(
	f"  Matching pairs with total score < 0: {combined_two_col_no_happy_neg_pairs}/{combined_two_col_no_happy_pairs} "
	f"({combined_two_col_no_happy_neg_pct:.1f}%)"
)
print(
	f"  Matching pairs with total score <= 0: {combined_two_col_no_happy_non_pos_pairs}/{combined_two_col_no_happy_pairs} "
	f"({combined_two_col_no_happy_non_pos_pct:.1f}%)"
)

if not is_suite:
	print()
	print("(Single pair mode: suite-level section still shown for consistency over one pair.)")

print()
print("###### Runtime ######")
print(f"  Parsing:  {timer_end_parsing - timer_start_parsing:.4f}s")
print(f"  Analysis: {timer_end_analysis - timer_start_analysis:.4f}s")
print(f"  Total:    {timer_end_analysis - timer_start_parsing:.4f}s")
