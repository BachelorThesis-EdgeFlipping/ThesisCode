import math
import random
import os
from collections import deque

from data_structures.Triangulation import Triangulation

def get_regular_polygon_points(n: int) -> list[tuple[float, float]]:
    points = []
    radius = 100.0
    center_x, center_y = radius, radius
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2 # start at top (pi/2)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points

def create_base_triangulation(n: int) -> Triangulation:
    tri = Triangulation()
    points = get_regular_polygon_points(n)
    tri.initialize_regular_polygon(points)
    # create a fan triangulation from vertex 0
    for i in range(2, n - 1):
        tri.insert_edge(0, i)
    return tri

def get_internal_edges(n: int, edge_set: set[tuple[int, int]]) -> list[list[int]]:
    internal = []
    for u, v in edge_set:
        diff = abs(u - v)
        if diff != 1 and diff != n - 1:
            internal.append([min(u, v), max(u, v)])
    return sorted(internal)

def catalan_number(n: int) -> int:
    if n < 3: return 0
    return math.comb(2 * (n - 2), n - 2) // (n - 1)

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

def discover_all_triangulations(n: int) -> list[list[list[int]]]:
    # Runs a full BFS over the flip graph to discover all distinct triangulations
    tri = create_base_triangulation(n)
    
    initial_internal_edges = tuple(tuple(e) for e in get_internal_edges(n, tri.edge_set()))
    visited = {initial_internal_edges}
    
    queue = deque([tri])
    results = []

    try:
        while queue:
            current = queue.popleft()
            
            current_internal_edges = get_internal_edges(n, current.edge_set())
            results.append(current_internal_edges)

            flippable = current.get_flippable_edges()
            for u, v in flippable:
                neighbor = current.deep_copy()
                can_flip = neighbor.flip_edge(u, v)
                if can_flip:
                    new_internal = tuple(tuple(e) for e in get_internal_edges(n, neighbor.edge_set()))
                    if new_internal not in visited:
                        visited.add(new_internal)
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
    print("=== Convex Polygon Triangulation Generator ===")
    num_vertices = get_int_input("1. Enter the number of vertices (order of the polygon): ", min_val=3)
    
    exact_num = catalan_number(num_vertices)
    print(f"-> A convex polygon with {num_vertices} vertices has exactly {exact_num} possible triangulations (calculated via Catalan number).")
    
    generate_all = get_bool_input(f"2. Do you want to generate ALL {exact_num} possible triangulations? (y/n, default n): ")
    
    num_triangulations = 0
    flips_range = (0, 0)
    
    if generate_all:
        if exact_num > 100000:
            print(f"\n[WARNING] Calculating ALL {exact_num} triangulations may take a massive amount of RAM, time, and disk space.")
            confirm = get_bool_input(f"Are you absolutely sure you want to proceed computing ALL triangulations? (y/n): ")
            if not confirm:
                print("Aborting.")
                return
    else:
        num_triangulations = get_int_input("2b. Enter how many distinct triangulations to generate: ", min_val=1)
        
        while True:
            val = input("3. Enter range for random flips as 'min max' (e.g., '5 15'): ").strip()
            parts = val.split()
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                flips_range = (int(parts[0]), int(parts[1]))
                if flips_range[0] <= flips_range[1]:
                    break
            print("Invalid range. Please provide two integers separated by a space (e.g. '5 15').")

    seed_str = input("4. Enter a random seed (or press Enter to randomize): ").strip()
    if seed_str.isdigit():
        global_seed = int(seed_str)
    else:
        global_seed = random.randint(0, 999999999)
        
    output_dir = input("5. Enter output directory path (or press Enter for 'data/convex_polygon/generated'): ").strip()
    if not output_dir:
        output_dir = "data/convex_polygon/generated"
        
    # --- Confirmation ---
    print("\n--- Configuration confirmed ---")
    print(f"Vertices (order): {num_vertices}")
    if generate_all:
        print("Triangulations to generate: ALL POSSIBLE")
    else:
        print(f"Triangulations to generate: {num_triangulations}")
        print(f"Random Flips Range: {flips_range[0]} to {flips_range[1]}")
    print(f"Global Seed: {global_seed}")
    print(f"Output Directory: {output_dir}")
    print("-------------------------------")
    if not get_bool_input("Start generating? (y/n): "):
        print("Aborting.")
        return

    # --- Execution ---
    random.seed(global_seed)
    
    if generate_all:
        folder_name = f"cp_{num_vertices}_ALL_{global_seed}"
    else:
        folder_name = f"cp_{num_vertices}_{flips_range[0]}-{flips_range[1]}_{global_seed}"
    
    actual_output_dir = os.path.join(output_dir, folder_name)
    os.makedirs(actual_output_dir, exist_ok=True)
    
    total_generated = 0
    total_duplicates = 0
    
    print(f"\nProcessing convex polygon of order {num_vertices}...")
    
    if generate_all:
        all_triangulations = discover_all_triangulations(num_vertices)
        for t, internal_edges in enumerate(all_triangulations):
            edges_str = ",\n    ".join(f"[{u}, {v}]" for u, v in internal_edges)
            json_str = f'{{\n  "order": {num_vertices},\n  "internal_edges": [\n    {edges_str}\n  ]\n}}'
            
            output_path = os.path.join(actual_output_dir, f"cp{num_vertices}_{t+1}.json")
            with open(output_path, "w") as f:
                f.write(json_str)

        gen_count = len(all_triangulations)
        print(f"  -> Discovered and saved {gen_count} total distinct triangulations.")
        total_generated += gen_count
    else:
        seen_edge_sets = set()
        duplicates_found = 0
        
        t = 0
        attempts = 0
        max_attempts = num_triangulations * 50  # Prevent infinite loop
        
        while t < num_triangulations and attempts < max_attempts:
            attempts += 1
            tri = create_base_triangulation(num_vertices)
            
            num_flips = random.randint(flips_range[0], flips_range[1])
            for _ in range(num_flips):
                flip_set = get_random_simultaneous_flip_set(tri)
                if not flip_set:
                    break
                tri.flip_edges_simultaneous(flip_set)
                
            internal_edges = get_internal_edges(num_vertices, tri.edge_set())
            edge_tuple = tuple(tuple(e) for e in internal_edges)
            
            if edge_tuple in seen_edge_sets:
                duplicates_found += 1
                tri.destroy()
                continue
            
            seen_edge_sets.add(edge_tuple)
            
            edges_str = ",\n    ".join(f"[{u}, {v}]" for u, v in internal_edges)
            json_str = f'{{\n  "order": {num_vertices},\n  "internal_edges": [\n    {edges_str}\n  ]\n}}'
            
            output_path = os.path.join(actual_output_dir, f"cp{num_vertices}_{t+1}.json")
            with open(output_path, "w") as f:
                f.write(json_str)
                
            print(f"Generated {output_path} with {num_flips} flip steps.")
            tri.destroy()
            t += 1
            
        total_generated += t
        total_duplicates += duplicates_found
            
        if attempts >= max_attempts:
            print(f"  -> Warning: Reached maximum attempts. Only generated {t} out of {num_triangulations} unique triangulations.")
            
        if duplicates_found > 0:
            print(f"  -> Note: Filtered out {duplicates_found} identical triangulation(s).")

    print("\n" + "="*40)
    print("Generation Summary:")
    print("="*40)
    print(f"Order of Polygon: {num_vertices}")
    print(f"Global seed: {global_seed}")
    if generate_all:
        print(f"Mode: ALL {exact_num} possible triangulations dynamically discovered")
    else:
        print(f"Total duplicate combinations dynamically rejected: {total_duplicates}")
        print(f"Total distinct triangulations requested: {num_triangulations}")
    print(f"Total distinct triangulations successfully generated: {total_generated}")
    print("="*40)

if __name__ == "__main__":
    main()