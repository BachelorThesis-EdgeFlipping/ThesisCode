import os
import json
import random
import re

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
    print("=== Suite Generator ===")
    
    # 1. Convex Polygon or Arbitrary Point Sets
    print("1. Choose geometry type:")
    print("  1) Convex Polygon (convex_polygon)")
    print("  2) Arbitrary Point Sets (point_set)")
    
    geom_choice = get_int_input("Enter choice (1 or 2): ", min_val=1)
    while geom_choice not in [1, 2]:
        print("Invalid choice.")
        geom_choice = get_int_input("Enter choice (1 or 2): ", min_val=1)
        
    is_point_set = (geom_choice == 2)
    base_dir = "data/point_set/generated" if is_point_set else "data/convex_polygon/generated"
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist yet. Please generate some triangulations first.")
        return
        
    # 2. Number of vertices
    num_vertices = get_int_input("2. Enter the number of vertices: ", min_val=3)
    
    folders = []
    for f in os.listdir(base_dir):
        fp = os.path.join(base_dir, f)
        # Search for folders that logically start with `{num_vertices}_` or `cp_{num_vertices}_`.
        if os.path.isdir(fp):
            if is_point_set and f.startswith(f"{num_vertices}_"):
                folders.append(f)
            elif not is_point_set and f.startswith(f"cp_{num_vertices}_"):
                folders.append(f)
            
    if not folders:
        print(f"No generation folders found for {num_vertices} vertices in {base_dir}.")
        return
        
    # 3. List available triangulation folders
    print("\n3. Available generation folders:")
    for i, folder in enumerate(folders):
        print(f"  {i+1}) {folder}")
        
    folder_idx = get_int_input("Choose a folder to create a suite for (enter number): ", min_val=1)
    while folder_idx < 1 or folder_idx > len(folders):
        print("Invalid folder number.")
        folder_idx = get_int_input("Choose a folder to create a suite for (enter number): ", min_val=1)
        
    chosen_folder = folders[folder_idx - 1]
    chosen_path = os.path.join(base_dir, chosen_folder)
    
    # Parse files inside the folder to figure out distinct vertex sets and triangulations
    files = [f for f in os.listdir(chosen_path) if f.endswith(".json")]
    
    groups = {}
    if is_point_set:
        # Expected e.g. rand7_1_1.json, rand7_1_2.json ... rand{N}_{S}_{T}.json
        for f in files:
            m = re.match(r"rand\d+_(\d+)_\d+\.json", f)
            if m:
                s_id = int(m.group(1))
                groups.setdefault(s_id, []).append(f)
            else:
                groups.setdefault(1, []).append(f) # fallback
    else:
        # For convex polygon we maybe just have fanN_T.json etc. 
        # But suppose there are multiple sets, too. Usually it's just one set (the polygon).
        for f in files:
            # If they follow the same N_S_T format, try it
            m = re.match(r"[a-zA-Z]+\d+_(\d+)_\d+\.json", f)
            if m:
                s_id = int(m.group(1))
                groups.setdefault(s_id, []).append(f)
            else:
                groups.setdefault(1, []).append(f)
        
    # Validation
    if not groups:
        print("No .json files found in the chosen folder.")
        return
        
    # Calculate possibilities
    set_possibilities = {}
    for s_id, flist in groups.items():
        k = len(flist)
        set_possibilities[s_id] = k * (k - 1) if k >= 2 else 0
        
    total_possible = sum(set_possibilities.values())
    if total_possible == 0:
        print("Not enough triangulations to form pairs! Need at least 2 triangulations in a set.")
        return
        
    print(f"\nFor selected folder '{chosen_folder}', there are {len(groups)} distinct vertex set(s).")
    
    print("\n4. Generate Pairs Configuration")
    generate_all = get_bool_input(f"Do you want to generate ALL possible problem pairs ({total_possible} total)? (y/n, default n): ")
    
    requested_pairs = 0
    if not generate_all:
        prompt_txt = "Enter how many problem pairs you want to generate per sequence/set: " if is_point_set and len(groups) > 1 else "Enter how many problem pairs to generate: "
        requested_pairs = get_int_input(prompt_txt, min_val=1)
        
    include_twins = False
    if not generate_all:
        include_twins = get_bool_input("Do you want to automatically include the 'twin' (reversed source/target) for each selected pair? (y/n, default n): ")
        
    # --- Pair Generation Logic ---
    all_sources = []
    all_targets = []
    total_generated = 0

    for s_id in sorted(groups.keys()):
        flist = groups[s_id]
        max_possible = set_possibilities[s_id]
        if max_possible == 0:
            continue
            
        # Create all possible unique pairs
        pairs = []
        for i in range(len(flist)):
            for j in range(len(flist)):
                if i != j:
                    pairs.append((flist[i], flist[j]))
                    
        # Filter or pick pairs
        if generate_all or requested_pairs >= max_possible:
            chosen_pairs = pairs
        else:
            chosen_pairs = random.sample(pairs, requested_pairs)
            
            if include_twins:
                chosen_set = set(chosen_pairs)
                extended_pairs = list(chosen_pairs)
                for src, tgt in chosen_pairs:
                    twin = (tgt, src)
                    if twin not in chosen_set:
                        extended_pairs.append(twin)
                        chosen_set.add(twin)
                chosen_pairs = extended_pairs
            
        for src, tgt in chosen_pairs:
            all_sources.append(src.replace(".json", ""))
            all_targets.append(tgt.replace(".json", ""))
            
        total_generated += len(chosen_pairs)

    twin_suffix = "_twins" if (include_twins or generate_all) else ""
    default_suite_name = f"{chosen_folder}_suite_n{total_generated}{twin_suffix}"
    suite_name = input(f"Enter a name for this suite (or press Enter for '{default_suite_name}'): ").strip()
    if not suite_name:
        suite_name = default_suite_name
    if not suite_name.endswith(".json"):
        suite_name += ".json"
        
    out_path = os.path.join("data", "suites", "generated", suite_name)
    
    # 5. Confirm
    print("\n--- Configuration confirmed ---")
    print(f"Target folder: {chosen_folder}")
    print(f"Geometry type: {"Point Set" if is_point_set else "Convex Polygon"}")
    if generate_all:
        print(f"Pairs to generate: ALL possible ({total_possible} total pairs)")
    else:
        twin_str = " (with twins)" if include_twins else ""
        if is_point_set and len(groups) > 1:
            print(f"Pairs to generate: {requested_pairs} max per set{twin_str} (Total capped at {total_possible})")
        else:
            print(f"Pairs to generate: {requested_pairs} max{twin_str} (Total capped at {total_possible})")
    print(f"Output File: {out_path}")
    print("-------------------------------")
    if not get_bool_input("5. Start saving? (y/n): "):
        print("Aborting.")
        return
        
    # Execution
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
    # Write JSON
    # path_prefix ignores "convex_polygon" and "point_set" distinction, it starts exactly at "generated/..." 
    path_prefix = f"generated/{chosen_folder}/"
    
    result = {
        "path_prefix": path_prefix,
        "sources": all_sources,
        "targets": all_targets
    }
    
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
        
    print("\n" + "="*40)
    print("Generation Summary:")
    print("="*40)
    print(f"Suite generated and saved to: {out_path}")
    print(f"Total problem pairs generated: {total_generated}")
    print("="*40)

if __name__ == "__main__":
    main()
