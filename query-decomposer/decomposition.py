import networkx as nx
from networkx.algorithms.approximation.treewidth import treewidth_min_fill_in


def run_decomposition(edges, tables):
    # --- Step 1: build the primal graph of the hypergraph ---
    G = nx.Graph()
    G.add_nodes_from({var for edge in edges.values() for var in edge})
    # every relation's variables become a clique
    for table in tables:
        vars_ = list(edges[table])
        for i in range(len(vars_)):
            for j in range(i + 1, len(vars_)):
                G.add_edge(vars_[i], vars_[j])

    # --- Step 2: min-fill tree decomposition ---
    treewidth, decomp = treewidth_min_fill_in(G) # networkx keeps one bag per eliminated vertex

    # --- Step 3: remove redundant bags ---
    changed = True
    while changed:
        changed = False
        for b in list(decomp.nodes()):
            # check if this bag is a subset of some neighbour (redundant) and take first such neigbour
            superset = next((a for a in decomp.neighbors(b) if b <= a), None) 
            if superset is not None:
                # connect every other neighbour of redundant bag to superset bag
                for nb in list(decomp.neighbors(b)):
                    if nb != superset:
                        decomp.add_edge(superset, nb)
                decomp.remove_node(b)
                changed = True
                # to start with new list of bag nodes due to removal
                break

    # --- Step 4: convert networkx output ---
    bag_id = {bag: i + 1 for i, bag in enumerate(decomp.nodes())}
    bags = {i: set(bag) for bag, i in bag_id.items()}          # bag_id -> set of variables
    tree_edges = [(bag_id[a], bag_id[b]) for a, b in decomp.edges()]

    return bags, tree_edges, treewidth


if __name__ == "__main__":
    edges_2 = {
        "LINEITEM": frozenset(["O_KEY", "S_KEY", "PARTKEY", "L_QUANTITY"]),
        "SUPPLIER": frozenset(["NATIONKEY", "S_KEY", "S_NAME"]),
        "CUSTOMER": frozenset(["NATIONKEY", "C_NAME", "CUSTKEY"]),
    }
    tables_2 = ["LINEITEM", "SUPPLIER", "CUSTOMER"]

    bags, tree_edges, treewidth = run_decomposition(edges_2, tables_2)

    print("=== Bags ===")
    for bag_id_, bag_vars in bags.items():
        print(f"  Bag {bag_id_}: {sorted(bag_vars)}")

    print("\n=== Tree edges ===")
    for a, b in tree_edges:
        print(f"  Bag {a} -- Bag {b}")

    print(f"\n=== Treewidth: {treewidth} ===")
