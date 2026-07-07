def orient_tree(bags, tree_edges, root):
    adjacency = {bag_id: [] for bag_id in bags}
    for (a, b) in tree_edges:
        adjacency[a].append(b)
        adjacency[b].append(a)

    children = {bag_id: [] for bag_id in bags}
    parent = {}
    visited = {root}
    stack = [root]

    while stack:
        bag_id = stack.pop()
        for neighbor in adjacency[bag_id]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = bag_id
                children[bag_id].append(neighbor)
                stack.append(neighbor)

    return children, parent


def compute_bridge_vars(bags, parent, root):
    bridge_vars = {}
    for bag_id in bags:
        if bag_id == root:
            continue
        bridge_vars[bag_id] = bags[bag_id] & bags[parent[bag_id]]
    return bridge_vars


def build_q_fragment(table, bag_vars, edges, var_to_col, predicates_list, alias_to_table):
    overlap = edges[table] & bag_vars
    if not overlap:
        return None   # table contributes nothing to this bag

    physical = alias_to_table.get(table, table)  # e.g, "R1" → "EDGES", "ORDERS" → "ORDERS"

    # check if all table vars in bag
    is_full = (overlap == edges[table])

    select_cols = []
    needs_rename = False
    for var in sorted(overlap):
        actual_col = var_to_col[(table, var)]
        if actual_col != var:
            select_cols.append(f"{actual_col} AS {var}")
            needs_rename = True
        else:
            select_cols.append(var)

    # full table + no renames + no filter → bare table reference
    if is_full and not needs_rename and not predicates_list:
        return physical, overlap

    where_clause = f" WHERE {' AND '.join(predicates_list)}" if predicates_list else ""

    if is_full and not needs_rename:
        sql = f"(SELECT * FROM {physical}{where_clause})"
    else:
        distinct = "" if is_full else "DISTINCT "
        sql = f"(SELECT {distinct}{', '.join(select_cols)} FROM {physical}{where_clause})"

    return sql, overlap


def build_q_view(bag_id, bags, tables, edges, var_to_col, predicates, alias_to_table):
    bag_vars = bags[bag_id]

    # collect all fragments that contribute to this bag
    fragments = []
    for table in tables:
        result = build_q_fragment(table, bag_vars, edges, var_to_col, predicates.get(table, []), alias_to_table)
        if result is not None:
            sql, overlap = result
            fragments.append((sql, overlap, table))

    # sort largest overlap first so accumulated grows as fast as possible
    fragments.sort(key=lambda f: len(f[1]), reverse=True)

    # start from the first fragment
    first_sql, first_overlap, _ = fragments[0]
    from_clause = first_sql
    accumulated = set(first_overlap)

    # attach each remaining fragment with JOIN USING the shared vars
    for frag_sql, frag_overlap, _ in fragments[1:]:
        shared = accumulated & frag_overlap      # only vars already on the left side
        using_cols = ", ".join(sorted(shared))
        from_clause += f"\nJOIN {frag_sql} USING ({using_cols})"
        accumulated |= frag_overlap              # add this fragment's vars to accumulated (union)

    return f"SELECT *\nFROM {from_clause}"


def generate_sql(tables, edges, var_to_col, bags, tree_edges, predicates, alias_to_table, root=1):

    # --- Step 1: orient the tree ---
    children, parent = orient_tree(bags, tree_edges, root)

    # --- Step 2: bridge variables ---
    bridge_vars = compute_bridge_vars(bags, parent, root)

    # --- Step 3: create views in post-order (children before parents) ---
    views = []

    def emit_views(bag_id):
        # recurse into children first for their P' views
        for child in children[bag_id]:
            emit_views(child)

        # build the Q relation 
        q_sql = build_q_view(bag_id, bags, tables, edges, var_to_col, predicates, alias_to_table)

        # extend Q with each child's P' view to get Q'
        q_prime_sql = q_sql
        for child in children[bag_id]:
            using_cols = ", ".join(sorted(bridge_vars[child]))
            q_prime_sql += f"\nJOIN BAG_{child}_PPRIME USING ({using_cols})"

        if bag_id == root:
            views.append(f"-- Root Bag.\nCREATE MATERIALIZED VIEW ROOT_QPRIME AS\n{q_prime_sql};")
        else:
            views.append(f"-- Bag {bag_id}.\nCREATE MATERIALIZED VIEW BAG_{bag_id}_QPRIME AS\n{q_prime_sql};")

            bridge_cols = ", ".join(sorted(bridge_vars[bag_id]))
            views.append(f"CREATE MATERIALIZED VIEW BAG_{bag_id}_PPRIME AS\nSELECT DISTINCT {bridge_cols} FROM BAG_{bag_id}_QPRIME;")

    emit_views(root)

    return views


if __name__ == "__main__":
    
    bags_2 = {
        1: {"S_KEY", "NATIONKEY", "S_NAME"},
        2: {"CUSTKEY", "C_NAME", "NATIONKEY"},
        3: {"L_QUANTITY", "O_KEY", "PARTKEY", "S_KEY"},
    }
    tree_edges_2 = [(1, 2), (1, 3)]

    schema_2 = {
        "LINEITEM": ["O_KEY", "PARTKEY", "S_KEY", "L_QUANTITY"],
        "SUPPLIER": ["SUPPKEY", "NATIONKEY", "S_NAME"],
        "CUSTOMER": ["CUSTKEY", "NATIONKEY", "C_NAME"],
    }
    edges_2 = {
        "LINEITEM": frozenset(["O_KEY", "S_KEY", "PARTKEY", "L_QUANTITY"]),
        "SUPPLIER": frozenset(["NATIONKEY", "S_KEY", "S_NAME"]),
        "CUSTOMER": frozenset(["NATIONKEY", "C_NAME", "CUSTKEY"]),
    }
    tables_2 = ["LINEITEM", "SUPPLIER", "CUSTOMER"]
    var_to_col_2 = {
        ("LINEITEM", "O_KEY"):      "O_KEY",
        ("LINEITEM", "PARTKEY"):    "PARTKEY",
        ("LINEITEM", "S_KEY"):      "S_KEY",
        ("LINEITEM", "L_QUANTITY"): "L_QUANTITY",
        ("SUPPLIER", "S_KEY"):      "SUPPKEY",
        ("SUPPLIER", "NATIONKEY"):  "NATIONKEY",
        ("SUPPLIER", "S_NAME"):     "S_NAME",
        ("CUSTOMER", "CUSTKEY"):    "CUSTKEY",
        ("CUSTOMER", "NATIONKEY"):  "NATIONKEY",
        ("CUSTOMER", "C_NAME"):     "C_NAME",
    }
    predicates_2 = {}

    views = generate_sql(tables_2, edges_2, var_to_col_2, bags_2, tree_edges_2, predicates_2)

    print("=== Generated SQL ===\n")
    for view_sql in views:
        print(view_sql)
        print()
