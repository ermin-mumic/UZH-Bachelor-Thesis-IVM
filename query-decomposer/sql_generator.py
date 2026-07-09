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


def build_q_fragment(table, bag_vars, edges, var_to_col, predicates_list, alias_to_table, strict_mode):
    overlap = edges[table] & bag_vars
    if not overlap:
        return None   # table contributes nothing to this bag

    physical = alias_to_table.get(table, table)  # e.g, "R1" → "EDGES", "ORDERS" → "ORDERS"

    # check if all table vars in bag
    is_full = (overlap == edges[table])
    if strict_mode and not is_full:
        return None   # strict variant: only include table if ALL its vars are in this bag

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


def build_q_view(bag_id, bags, tables, edges, var_to_col, predicates, alias_to_table, strict_mode):
    bag_vars = bags[bag_id]

    # collect all fragments that contribute to this bag
    fragments = []
    for table in tables:
        result = build_q_fragment(table, bag_vars, edges, var_to_col, predicates.get(table, []), alias_to_table, strict_mode)
        if result is not None:
            sql, overlap = result
            fragments.append((sql, overlap, table))

    if not fragments:
        # no fragments, no accumulated join variables
        return None, set()

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
        accumulated |= frag_overlap

    # return SQL and the set of variables Q actually covers (may be subset of bag in strict mode)
    return f"SELECT *\nFROM {from_clause}", accumulated


def generate_sql(tables, edges, var_to_col, bags, tree_edges, predicates, alias_to_table, root=1, strict_mode=False, agg_type="STAR", special_col=None):

    # aggregate mode: each P' view carries an ANNOTATION_<bag> column and the result is a
    # single scalar instead of the reconstructed join.
    # COUNT(*) uses the (+, x) semiring with an implicit local annotation of 1 per row.
    aggregate = agg_type != "STAR"

    def annotation_expr(child_ids):
        # a bag's annotation = SUM over its Q' rows of (local annotation x product of child annotations).
        # for COUNT(*) the local annotation is 1, so a leaf bag is just COUNT(*).
        if child_ids:
            return "SUM(" + " * ".join(f"ANNOTATION_{c}" for c in child_ids) + ")"
        return "COUNT(*)"

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

        # build the Q relation; returns (sql, covered_vars) or (None, set()) for bags with no Q relation
        q_sql, q_vars = build_q_view(bag_id, bags, tables, edges, var_to_col, predicates, alias_to_table, strict_mode)

        if q_sql is None and not children[bag_id]:
            raise ValueError(f"Bag {bag_id} has no contributing tables and no children in strict mode.")

        # extend Q to get Q'
        # always use accumulated & bridge_vars[child] for USING:
        # - non-strict: q_vars = all bag vars, so intersection = bridge_vars[child]
        # - strict: q_vars may be subset of bag vars, intersection avoids referencing missing columns
        if q_sql is None:
            # start from first child's P' view
            first_child, *rest_children = children[bag_id]
            q_prime_sql = f"SELECT *\nFROM BAG_{first_child}_PPRIME"
            accumulated = set(bridge_vars[first_child])
            child_list = rest_children
        else:
            q_prime_sql = q_sql
            accumulated = set(q_vars)
            child_list = children[bag_id]

        for child in child_list:
            shared = accumulated & bridge_vars[child]
            using_cols = ", ".join(sorted(shared))
            q_prime_sql += f"\nJOIN BAG_{child}_PPRIME USING ({using_cols})"
            accumulated |= bridge_vars[child]

        if bag_id == root:
            views.append(f"-- Root Bag.\nCREATE MATERIALIZED VIEW ROOT_QPRIME AS\n{q_prime_sql};")
        else:
            views.append(f"-- Bag {bag_id}.\nCREATE MATERIALIZED VIEW BAG_{bag_id}_QPRIME AS\n{q_prime_sql};")

            bridge_cols = ", ".join(sorted(bridge_vars[bag_id]))
            if aggregate:
                views.append(f"CREATE MATERIALIZED VIEW BAG_{bag_id}_PPRIME AS\nSELECT {bridge_cols}, {annotation_expr(children[bag_id])} AS ANNOTATION_{bag_id}\nFROM BAG_{bag_id}_QPRIME\nGROUP BY {bridge_cols};")
            else:
                views.append(f"CREATE MATERIALIZED VIEW BAG_{bag_id}_PPRIME AS\nSELECT DISTINCT {bridge_cols} FROM BAG_{bag_id}_QPRIME;")

    emit_views(root)

    # --- Step 4: Result view ---
    if aggregate:
        # single scalar
        views.append(f"-- Aggregation Result.\nCREATE MATERIALIZED VIEW RESULT AS\nSELECT {annotation_expr(children[root])} AS RESULT FROM ROOT_QPRIME;")
    else:
        # full result: rejoin all bags' Q' relations top-down on bridge variables
        reconstruction_joins = []

        def dfs_reconstruction(bag_id):
            for child in children[bag_id]:
                using_cols = ", ".join(sorted(bridge_vars[child]))
                reconstruction_joins.append(f"JOIN BAG_{child}_QPRIME USING ({using_cols})")
                dfs_reconstruction(child)

        dfs_reconstruction(root)

        if reconstruction_joins:
            from_clause = "ROOT_QPRIME\n" + "\n".join(reconstruction_joins)
        else:
            # only 1 bag in decomposition (nothin to rejoin)
            from_clause = "ROOT_QPRIME"

        views.append(f"-- Full Result.\nCREATE MATERIALIZED VIEW RESULT AS\nSELECT * FROM {from_clause};")

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

    alias_to_table_2 = {}

    views = generate_sql(tables_2, edges_2, var_to_col_2, bags_2, tree_edges_2, predicates_2, alias_to_table_2)

    print("=== Generated SQL ===\n")
    for view_sql in views:
        print(view_sql)
        print()
