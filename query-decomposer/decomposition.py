import random

import networkx as nx
from networkx.algorithms.approximation.treewidth import treewidth_min_fill_in

from fhw import compute_fhw

# number of randomized node insertions
N_SAMPLES = 20


def _decompose_with_order(edges, tables, node_order):
    # --- Step 1: build the primal graph, inserting nodes in the given order ---
    # min-fill breaks ties by node insertion order
    G = nx.Graph()
    G.add_nodes_from(node_order)
    for table in tables:
        vars_ = sorted(edges[table])  # every relation's variables become a clique
        for i in range(len(vars_)):
            for j in range(i + 1, len(vars_)):
                G.add_edge(vars_[i], vars_[j])

    # --- Step 2: min-fill tree decomposition ---
    treewidth, decomp = treewidth_min_fill_in(G)  # networkx keeps one bag per eliminated vertex

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


def run_decomposition(edges, tables):
    # sample several insertion orderings and keep the one with the smallest fhw.
    all_vars = sorted({var for edge in edges.values() for var in edge})

    # candidate orderings: sorted baseline first, then N seeded shuffles
    orderings = [all_vars]
    for seed in range(N_SAMPLES):
        order = all_vars[:]
        random.Random(seed).shuffle(order)
        orderings.append(order)

    best = None  # (fhw, treewidth, bags, tree_edges)
    for order in orderings:
        bags, tree_edges, treewidth = _decompose_with_order(edges, tables, order)
        fhw = compute_fhw(bags, edges)
        # select min fhw, then min treewidth
        if best is None or (fhw, treewidth) < (best[0], best[1]):
            best = (fhw, treewidth, bags, tree_edges)

    _, treewidth, bags, tree_edges = best
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
