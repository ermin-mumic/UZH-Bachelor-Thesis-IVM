import subprocess
import os

HTD_BINARY = os.path.join(os.path.dirname(__file__), "..", "htd", "build", "bin", "htd_main-1.2.0")


def run_htd(edges, tables):
    # --- Step 1: assign integer ID to every canonical variable name ---

    all_vars = sorted({var for edge in edges.values() for var in edge})
    var_to_id = {var: i + 1 for i, var in enumerate(all_vars)}
    id_to_var = {i + 1: var for i, var in enumerate(all_vars)}

    # --- Step 2: build the hgr string ---
    num_vertices = len(all_vars)
    num_edges    = len(tables)

    lines = [f"p tw {num_vertices} {num_edges}"]
    for table in tables:
        vertex_ids = sorted(var_to_id[var] for var in edges[table])
        lines.append(" ".join(str(v) for v in vertex_ids))

    hgr_string = "\n".join(lines)

    # --- Step 3: run htd ---
    result = subprocess.run(
        [HTD_BINARY, "--type", "tree", "--input", "hgr", "--output", "td", "--opt", "width"],
        input=hgr_string,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"htd failed:\n{result.stderr}")

    # --- Step 4: parse the td output ---
    # Output format:
    #   s td <num_bags> <max_bag_size> <num_vertices>   
    #   b <bag_id> <v1> <v2> ...                       
    #   <bag_id1> <bag_id2>                            

    bags = {}        # bag_id (int) -> set of canonical variable names
    tree_edges = []  # list of (bag_id, bag_id) pairs
    treewidth = None

    for line in result.stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "s":
            treewidth = int(parts[3]) - 1  
        elif parts[0] == "b":
            bag_id = int(parts[1])
            bag_vars = {id_to_var[int(v)] for v in parts[2:]}
            bags[bag_id] = bag_vars
        else:
            tree_edges.append((int(parts[0]), int(parts[1])))

    return bags, tree_edges, treewidth


if __name__ == "__main__":
    edges_2 = {
        "LINEITEM": frozenset(["O_KEY", "S_KEY", "PARTKEY", "L_QUANTITY"]),
        "SUPPLIER": frozenset(["NATIONKEY", "S_KEY", "S_NAME"]),
        "CUSTOMER": frozenset(["NATIONKEY", "C_NAME", "CUSTKEY"]),
    }
    tables_2 = ["LINEITEM", "SUPPLIER", "CUSTOMER"]

    bags, tree_edges, treewidth = run_htd(edges_2, tables_2)

    print("=== Bags ===")
    for bag_id, bag_vars in bags.items():
        print(f"  Bag {bag_id}: {sorted(bag_vars)}")

    print("\n=== Tree edges ===")
    for a, b in tree_edges:
        print(f"  Bag {a} -- Bag {b}")

    print(f"\n=== Treewidth: {treewidth} ===")
