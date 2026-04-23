from io_utils.Parser import Parser
from Models import PointSetTriangulation
from data_structures.Triangulation import Triangulation
from ExhaustiveSearchAlgorithm import exhaustive_simultanious_flip_graph_search
import time

def parse_with_boundary(file_path: str) -> Triangulation:
    model = PointSetTriangulation.from_json(Parser.getJSONString(file_path))
    points = model.vertices
    edges = model.edges
    
    # Boundary edges of the capped channel polygon in order
    boundary_cycle = [0, 1, 2, 3, 4, 9, 8, 7, 6, 5, 10]
    for i in range(len(boundary_cycle)):
        v1 = boundary_cycle[i]
        v2 = boundary_cycle[(i + 1) % len(boundary_cycle)]
        edges.append([min(v1, v2), max(v1, v2)])
    
    tri = Triangulation()
    tri.initialize_from_edges(points, edges)
    tri.sanity_check()
    return tri

def run_pair_test(name: str, file_a: str, file_b: str):
    print(f"\n{'='*50}")
    print(f"Testing Pair: {name}")
    print(f"{'='*50}")
    
    # 1. Not flipping happy edges (ignore_happy_edges=True)
    print("1. Not flipping happy edges")
    tri_a_ignore = parse_with_boundary(file_a)
    tri_b_ignore = parse_with_boundary(file_b)
    t0 = time.time()
    paths_ignore, to_ignore = exhaustive_simultanious_flip_graph_search(
        tri_a_ignore, tri_b_ignore,
        ignore_happy_edges=True,
        timeout=1200
    )
    t1 = time.time()
    
    if to_ignore:
        print(f"  Timeout reached after {t1 - t0:.2f}s!")
    elif paths_ignore is None or len(paths_ignore) == 0:
        print(f"  No valid sequence found! ({t1 - t0:.2f}s)")
    else:
        print(f"  Done in {t1 - t0:.2f}s")
        print(f"  Sequence length:     {len(paths_ignore[0])}")
        print(f"  Number of sequences: {len(paths_ignore)}")
         
    # 2. Flipping happy edges (ignore_happy_edges=False)
    print("\n2. Flipping happy edges")
    tri_a_all = parse_with_boundary(file_a)
    tri_b_all = parse_with_boundary(file_b)
    
    t2 = time.time()
    paths_all, to_all = exhaustive_simultanious_flip_graph_search(
        tri_a_all, tri_b_all,
        ignore_happy_edges=False,
        timeout=1200
    )
    t3 = time.time()

    if to_all:
        print(f"  Timeout reached after {t3 - t2:.2f}s!")
    elif paths_all is None or len(paths_all) == 0:
        print(f"  No valid sequence found! ({t3 - t2:.2f}s)")
    else:
        print(f"  Done in {t3 - t2:.2f}s")
        print(f"  Sequence length:     {len(paths_all[0])}")
        print(f"  Number of sequences: {len(paths_all)}")


def run_test():
    left_file = "point_set/cap_channel_left.json"
    right_file = "point_set/cap_channel_right.json"
    canonical_file = "point_set/canonical_channel.json"
    
    run_pair_test("Left to Right", left_file, right_file)
    run_pair_test("Left to Canonical", left_file, canonical_file)
    run_pair_test("Canonical to Right", canonical_file, right_file)

if __name__ == '__main__':
    run_test()
