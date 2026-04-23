import os
import json
import argparse

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

def format_edges(edges):
    # Return sorted list of edges as [u, v] where u < v
    normalized = [ [min(e), max(e)] for e in edges ]
    return sorted(list(normalized))

def add_edge(edges_set, u, v):
    edges_set.add((min(u, v), max(u, v)))

def main():
    print("=== Point Set Triangulation Generator (Capped Channels) ===")
    max_m = get_int_input("Enter the maximum parameter m (number of vertices per row): ", min_val=2)
    
    default_dir = f"data/capped_channel/generated/run_m{max_m}"
    output_dir = input(f"Enter output directory path (or press Enter for '{default_dir}'): ").strip()
    if not output_dir:
        output_dir = default_dir
        
    create_suite = input("Automatically create a suite linking these left (source) -> right (target) pairs? (y/n, default y): ").strip().lower() != 'n'
        
    os.makedirs(output_dir, exist_ok=True)
    
    suite_sources = []
    suite_targets = []
    
    for m in range(2, max_m + 1):
        # Generate vertices
        # u_0 ... u_{m-1}  (Row 1, Y=0)
        # v_0 ... v_{m-1}  (Row 2, Y=60)
        # w                (Single vertex, X=0, Y=30)
        
        vertices = []
        
        # 0 to m-1: Row 1 (u)
        for i in range(1, m + 1):
            vertices.append((i * 20, 0))
            
        # m to 2m-1: Row 2 (v)
        for i in range(1, m + 1):
            vertices.append((i * 20, 60))
            
        # 2m: w
        w_idx = 2 * m
        vertices.append((0, 30))

        u_indices = list(range(0, m))
        v_indices = list(range(m, 2 * m))

        # Base Convex Hull Edges
        hull_edges = set()
        # w to u_0
        hull_edges.add((w_idx, u_indices[0]))
        # u_i to u_{i+1}
        for i in range(m - 1):
            hull_edges.add((u_indices[i], u_indices[i+1]))
        # u_{m-1} to v_{m-1}
        hull_edges.add((u_indices[-1], v_indices[-1]))
        # v_i to v_{i+1}
        for i in range(m - 1):
            hull_edges.add((v_indices[i], v_indices[i+1]))
        # w to v_0
        hull_edges.add((w_idx, v_indices[0]))

        # --- Triangulation 1 (Left Inclined) ---
        t1_edges = set()
        for e in hull_edges:
            add_edge(t1_edges, e[0], e[1])

        # Triangle with w, u_0, v_0
        add_edge(t1_edges, u_indices[0], v_indices[0])

        # First vertex of upper chain connects to every vertex of second row
        for vi in v_indices:
            add_edge(t1_edges, u_indices[0], vi)
            
        # Last vertex of second row, connects to every vertex of the first row
        for ui in u_indices:
            add_edge(t1_edges, v_indices[-1], ui)

        # --- Triangulation 2 (Right Inclined) ---
        t2_edges = set()
        for e in hull_edges:
            add_edge(t2_edges, e[0], e[1])

        add_edge(t2_edges, u_indices[0], v_indices[0])

        # First vertex of the second row with all the vertices of the first row
        for ui in u_indices:
            add_edge(t2_edges, v_indices[0], ui)
            
        # Last vertex of the first row with all the vertices of the second row
        for vi in v_indices:
            add_edge(t2_edges, u_indices[-1], vi)

        # Generate JSONs
        t1_file = os.path.join(output_dir, f"{m}_cc_l.json")
        t2_file = os.path.join(output_dir, f"{m}_cc_r.json")
        
        t1_json = {
            "vertices": vertices,
            "edges": format_edges(t1_edges)
        }
        t2_json = {
            "vertices": vertices,
            "edges": format_edges(t2_edges)
        }
        
        with open(t1_file, "w") as f:
            json.dump(t1_json, f, indent=4)
            
        with open(t2_file, "w") as f:
            json.dump(t2_json, f, indent=4)

        print(f"Generated {t1_file} and {t2_file} with {len(t1_edges)} and {len(t2_edges)} edges respectively.")
        
        suite_sources.append(f"{m}_cc_l")
        suite_targets.append(f"{m}_cc_r")

    if create_suite:
        suite_dir = "data/suites/generated"
        os.makedirs(suite_dir, exist_ok=True)
        
        path_prefix = ""
        output_normalized = output_dir.replace("\\", "/")
        if "data/capped_channel/" in output_normalized:
            path_prefix = output_normalized.split("data/capped_channel/")[-1]
            if not path_prefix.endswith("/"):
                path_prefix += "/"
        else:
            path_prefix = output_normalized + "/"

        suite_json = {
            "path_prefix": path_prefix,
            "sources": suite_sources,
            "targets": suite_targets
        }
        
        suite_file = os.path.join(suite_dir, f"capped_channel_{max_m}.json")
        with open(suite_file, "w") as f:
            json.dump(suite_json, f, indent=4)
        print(f"Generated suite {suite_file} linking pairs 2 to {max_m}.")

if __name__ == "__main__":
    main()
