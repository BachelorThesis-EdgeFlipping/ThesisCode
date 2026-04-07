import math
import random
import os
import copy
from collections import deque
from scipy.spatial import Delaunay
import numpy as np

from Models import PointSetTriangulation
from data_structures.Triangulation import Triangulation

def generate_random_point_set(num_vertices: int, limit: int = 100) -> list[tuple[int, int]]:
    pts = set()
    while len(pts) < num_vertices:
        pts.add((random.randint(0, limit), random.randint(0, limit)))
    return list(pts)

def get_delaunay_edges(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    del_tri = Delaunay(points)
    edges = set()
    for simplex in del_tri.simplices:
        for i in range(3):
            u, v = simplex[i], simplex[(i + 1) % 3]
            edges.add((min(u, v), max(u, v)))
    return list(edges)

def get_random_simultaneous_flip_set(tri: Triangulation) -> list[tuple[int, int]]:
    flippable = tri.get_flippable_edges()
    if not flippable:
        return []
    
    random.shuffle(flippable)
    
    edge_face_map = {}
    for v1, v2 in flippable:
        he = tri.find_edge_by_ids(v1, v2)
        edge_face_map[(v1, v2)] = (he.face.id, he.twin.face.id)
        
    chosen = []
    used_faces = set()
    for e in flippable:
        f1, f2 = edge_face_map[e]
        if f1 not in used_faces and f2 not in used_faces:
            if random.random() < 0.5:
                chosen.append(e)
                used_faces.add(f1)
                used_faces.add(f2)
                
    if not chosen and flippable:
        e = flippable[0]
        chosen.append(e)
        
    return chosen

def estimate_catalan(n: int) -> int:
    if n < 3: return 0
    return math.comb(2 * (n - 2), n - 2) // (n - 1)

def discover_all_triangulations(points: list[tuple[int, int]], base_edges: list[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    # Runs a full BFS over the flip graph to discover all distinct triangulations for a fixed point set
    tri = Triangulation()
    tri.initialize_from_edges(points, base_edges)

    initial_edges = frozenset(tuple(sorted([min(u, v), max(u, v)])) for u, v in tri.edge_set())
    visited = {initial_edges}
    
    queue = deque([tri])
    results = []

    try:
        while queue:
            current = queue.popleft()
            
            current_edges = sorted([list(e) for e in current.edge_set()])
            results.append(current_edges)

            flippable = current.get_flippable_edges()
            for u, v in flippable:
                neighbor = current.deep_copy()
                can_flip = neighbor.flip_edge(u, v)
                if can_flip:
                    new_edges = frozenset(tuple(sorted([min(x, y), max(x, y)])) for x, y in neighbor.edge_set())
                    if new_edges not in visited:
                        visited.add(new_edges)
                        queue.append(neighbor)
                    else:
                        neighbor.destroy()
                else:
                    neighbor.destroy()

            if current is not tri:
                current.destroy()
    finally:
        tri.destroy()
        
    return results

def get_int_input(prompt: str, min_val: int = None, default: int = None) -> int:
    while True:
        val = input(prompt).strip()
        if not val and default is not None:
            return default
        try:
            num = int(val)
            if min_val is not None and num < min_val:
                print(f"Please enter a number >= {min_val}.")
                continue
            return num
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_bool_input(prompt: str) -> bool:
    while True:
        val = input(prompt).strip().lower()
        if val in ('y', 'yes'):
            return True
        if val in ('n', 'no'):
            return False
        if not val:
            return False
        print("Please answer y or n.")

def main():
    print("=== Random Point Set Triangulation Generator ===")
    num_vertices = get_int_input("1. Enter the number of vertices per set: ", min_val=3)
    num_vertex_sets = get_int_input("2. Enter how many distinct sets of vertices to generate: ", min_val=1)
    
    estimate = estimate_catalan(num_vertices)
    generate_all = get_bool_input(f"3. Do you want to generate ALL possible triangulations for each vertex set (up to ~{estimate} for convex bound)? (y/n, default n): ")
    
    num_triangulations_per_set = 0
    flips_range = (0, 0)
    
    if generate_all:
        if num_vertices > 12:
            print(f"\n[WARNING] Calculating ALL triangulations for N={num_vertices} (up to ~{estimate}) may take a massive amount of RAM, time, and disk space.")
            confirm = get_bool_input(f"Are you absolutely sure you want to proceed computing ALL triangulations? (y/n): ")
            if not confirm:
                print("Aborting.")
                return
    else:
        num_triangulations_per_set = get_int_input("3b. Enter how many distinct triangulations to generate per distinct set of vertices: ", min_val=1)
        
        while True:
            val = input("4. Enter range for random flips as 'min max' (e.g., '5 15'): ").strip()
            parts = val.split()
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                flips_range = (int(parts[0]), int(parts[1]))
                if flips_range[0] <= flips_range[1]:
                    break
            print("Invalid range. Please provide two integers separated by a space (e.g. '5 15').")

    seed_str = input("5. Enter a random seed (or press Enter to randomize): ").strip()
    if seed_str.isdigit():
        global_seed = int(seed_str)
    else:
        global_seed = random.randint(0, 999999999)
        
    output_dir = input("6. Enter output directory path (or press Enter for 'data/point_set/generated'): ").strip()
    if not output_dir:
        output_dir = "data/point_set/generated"
        
    # --- Confirmation ---
    print("\n--- Configuration confirmed ---")
    print(f"Vertices per set: {num_vertices}")
    print(f"Number of distinct vertex sets: {num_vertex_sets}")
    if generate_all:
        print("Triangulations per set: ALL POSSIBLE")
    else:
        print(f"Triangulations per set: {num_triangulations_per_set}")
        print(f"Random Flips Range: {flips_range[0]} to {flips_range[1]}")
    print(f"Global Seed: {global_seed}")
    print(f"Output Directory: {output_dir}")
    print("-------------------------------")
    if not get_bool_input("Start generating? (y/n): "):
        print("Aborting.")
        return

    # --- Execution ---
    random.seed(global_seed)
    np.random.seed(global_seed)
    
    if generate_all:
        folder_name = f"{num_vertices}_{num_vertex_sets}_ALL_{global_seed}"
    else:
        folder_name = f"{num_vertices}_{num_vertex_sets}_{flips_range[0]}-{flips_range[1]}_{global_seed}"
    
    actual_output_dir = os.path.join(output_dir, folder_name)
    os.makedirs(actual_output_dir, exist_ok=True)
    
    total_generated = 0
    total_duplicates = 0
    triangulations_per_set = []
    
    for s in range(num_vertex_sets):
        print(f"\nProcessing vertex set {s+1}/{num_vertex_sets}...")
        points = generate_random_point_set(num_vertices, 100)
        base_edges = get_delaunay_edges(points)
        
        if generate_all:
            all_triangulations = discover_all_triangulations(points, base_edges)
            for t, current_edges in enumerate(all_triangulations):
                points_list = [list(p) for p in points]
                vertices_str = ",\n    ".join(f"[{x}, {y}]" for x, y in points_list)
                edges_str = ",\n    ".join(f"[{u}, {v}]" for u, v in current_edges)
                json_str = f'{{\n  "vertices": [\n    {vertices_str}\n  ],\n  "edges": [\n    {edges_str}\n  ],\n  "seed": {global_seed}\n}}'
                
                output_path = os.path.join(actual_output_dir, f"rand{num_vertices}_{s+1}_{t+1}.json")
                with open(output_path, "w") as f:
                    f.write(json_str)

            gen_count = len(all_triangulations)
            print(f"  -> Discovered and saved {gen_count} total distinct triangulations.")
            triangulations_per_set.append(gen_count)
            total_generated += gen_count
        else:
            seen_edge_sets = set()
            duplicates_found = 0
            
            t = 0
            attempts = 0
            max_attempts = num_triangulations_per_set * 50  # Prevent infinite loop on small point sets limit
            
            while t < num_triangulations_per_set and attempts < max_attempts:
                attempts += 1
                tri = Triangulation()
                tri.initialize_from_edges(points, base_edges)
                
                num_flips = random.randint(flips_range[0], flips_range[1])
                for _ in range(num_flips):
                    flip_set = get_random_simultaneous_flip_set(tri)
                    if not flip_set:
                        break
                    tri.flip_edges_simultaneous(flip_set)
                    
                edge_set = frozenset(tuple(sorted([min(u, v), max(u, v)])) for u, v in tri.edge_set())
                if edge_set in seen_edge_sets:
                    duplicates_found += 1
                    tri.destroy()
                    continue
                
                seen_edge_sets.add(edge_set)
                
                current_edges = sorted([list(e) for e in edge_set])
                points_list = [list(p) for p in points]
                
                vertices_str = ",\n    ".join(f"[{x}, {y}]" for x, y in points_list)
                edges_str = ",\n    ".join(f"[{u}, {v}]" for u, v in current_edges)
                json_str = f'{{\n  "vertices": [\n    {vertices_str}\n  ],\n  "edges": [\n    {edges_str}\n  ],\n  "seed": {global_seed}\n}}'
                
                output_path = os.path.join(actual_output_dir, f"rand{num_vertices}_{s+1}_{t+1}.json")
                with open(output_path, "w") as f:
                    f.write(json_str)
                    
                print(f"Generated {output_path} with {num_flips} flip steps.")
                tri.destroy()
                t += 1
                
            triangulations_per_set.append(t)
            total_generated += t
            total_duplicates += duplicates_found
                
            if attempts >= max_attempts:
                print(f"  -> Warning: Reached maximum attempts for point set {s+1}. Only generated {t} out of {num_triangulations_per_set} unique triangulations.")
                
            if duplicates_found > 0:
                print(f"  -> Note: Filtered out {duplicates_found} identical triangulation(s) for point set {s+1}.")

    print("\n" + "="*40)
    print("Generation Summary:")
    print("="*40)
    print(f"Total distinct vertex sets: {num_vertex_sets}")
    print(f"Vertices per set: {num_vertices}")
    print(f"Global seed: {global_seed}")
    if generate_all:
        print(f"Mode: ALL possible triangulations dynamically discovered")
    else:
        print(f"Total duplicate combinations dynamically rejected: {total_duplicates}")
        print(f"Total distinct triangulations requested: {num_vertex_sets * num_triangulations_per_set}")
    print(f"Total distinct triangulations successfully generated: {total_generated}")
    print("-" * 40)
    for i, count in enumerate(triangulations_per_set):
        print(f"  Point set {i+1}: {count} triangulations")
    print("="*40)

if __name__ == "__main__":
    main()
