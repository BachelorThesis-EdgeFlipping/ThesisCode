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


SOURCE_FILE = "counterexample_DDAG_source"
TARGET_FILE = "counterexample_DDAG_target"
DATA_FOLDER = "convex_polygon/"
source = ConvexPolygonTriangulationParser.parse(f"{DATA_FOLDER}{SOURCE_FILE}.json")
target = ConvexPolygonTriangulationParser.parse(f"{DATA_FOLDER}{TARGET_FILE}.json")

def print_paths_info(name: str, paths: list[list[StepData]] | None, time_taken: float, timed_out: bool):
    print(f"--- {name} ---")
    if timed_out:
        print("Search timed out.")
        return
    if not paths:
        print("No paths found.")
        return
    
    print(f"Search found {len(paths)} optimal path(s) of length {len(paths[0])} in {time_taken:.4f}s.")
    for i, path in enumerate(paths, 1):
        print(f"Path {i}:")
        for step_idx, step in enumerate(path):
            flips = ", ".join(f"({e[0]},{e[1]})" for e in step.flip_set)
            print(f"  Step {step_idx + 1}: flips={{{flips}}}")
    print()

def main():
    print(f"Comparing paths for: {SOURCE_FILE} -> {TARGET_FILE}")
    # 1. Single flip only
    start = time.time()
    single_paths, timed_out_single = exhaustive_simultanious_flip_graph_search(
        source, target, only_single_flips=True
    )
    time_single = time.time() - start
    print_paths_info("Single Flips Only", single_paths, time_single, timed_out_single)
    # 2. Allow multiple flips (simultaneous)
    start = time.time()
    multi_paths, timed_out_multi = exhaustive_simultanious_flip_graph_search(
        source, target, only_single_flips=False
    )
    time_multi = time.time() - start
    print_paths_info("Multiple Flips Allowed", multi_paths, time_multi, timed_out_multi)
    print("--- Comparison ---")
    if single_paths and multi_paths:
        def get_all_flips(paths):
            path_flips = []
            for path in paths:
                flips = set()
                for step in path:
                    for e in step.flip_set:
                        flips.add(f"({e[0]},{e[1]})")
                path_flips.append(flips)
            return path_flips
        single_flips_per_path = get_all_flips(single_paths)
        multi_flips_per_path = get_all_flips(multi_paths)

        print("Single Flips Only Paths (Unique flips used per path):")
        for i, flips in enumerate(single_flips_per_path, 1):
            print(f"  Path {i} used flips: {{{', '.join(sorted(flips))}}}")
        print("\nMultiple Flips Allowed Paths (Unique flips used per path):")
        for i, flips in enumerate(multi_flips_per_path, 1):
            print(f"  Path {i} used flips: {{{', '.join(sorted(flips))}}}")  
        print("\nChecking if Single-Flip paths contain all flips of Multi-Flip paths:")
        for i, s_flips in enumerate(single_flips_per_path, 1):
            for j, m_flips in enumerate(multi_flips_per_path, 1):
                contains_all = m_flips.issubset(s_flips)
                print(f"  Single-Flip Path {i} contains all flips of Multi-Flip Path {j}: {contains_all}")
    else:
        print("Could not compare because one or both searches timed out or found no paths.")

if __name__ == "__main__":
    main()

