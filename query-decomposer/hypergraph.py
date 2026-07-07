def build_hypergraph(combined_schema, tables, joins, alias_to_table):
    # 1. UNION FIND ALGORITHM
    # every (table, col) starts as own group (only for tables part of the query)
    parent = {}
    for table in tables:
        for col in combined_schema[table]:
            parent[(table, col)] = (table, col)   # every (table, col) is its own root

    #find the root of x's group
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])  
        return parent[x]

    # merge groups of x and y
    def union(x, y):
        rx = find(x)
        ry = find(y)
        if rx != ry:
            parent[ry] = rx   

    # apply all join conditions
    for (lt, lc, rt, rc) in joins:
        union((lt, lc), (rt, rc))


    roots = {find(key) for key in parent}

    col_name_counts = {}
    for (tbl, col) in roots:
        col_name_counts[col] = col_name_counts.get(col, 0) + 1

    # If a column name is unique among roots -> use it as-is.
    # If two different roots share the same column name -> prefix with table name.
    def canonical(root):
        tbl, col = root
        return f"{tbl}_{col}" if col_name_counts[col] > 1 else col

    # col_to_var:  (table, col) -> canonical name of root to build hyperedges
    # var_to_col:  (table, canonical name) -> actual physical col name used in SQL generation
    col_to_var = {}
    var_to_col = {}
    for (table, col) in parent:
        root = find((table, col))
        canon = canonical(root)
        col_to_var[(table, col)] = canon
        phys_table = alias_to_table.get(table, table)
        phys_cols  = combined_schema[phys_table]
        vars_list  = combined_schema[table]
        var_to_col[(table, canon)] = phys_cols[vars_list.index(col)]

    edges = {}
    for table in tables:
        edges[table] = frozenset(col_to_var[(table, col)] for col in combined_schema[table])

    return col_to_var, var_to_col, edges


if __name__ == "__main__":
    schema_1 = {
        "LINEITEM": ["ORDERKEY", "PARTKEY", "SUPPKEY", "L_QUANTITY"],
        "SUPPLIER": ["SUPPKEY", "NATIONKEY", "S_NAME"],
        "CUSTOMER": ["CUSTKEY", "NATIONKEY", "C_NAME"],
    }

    tables_1 = ["LINEITEM", "SUPPLIER", "CUSTOMER"]

    joins_1 = [
        ("LINEITEM", "SUPPKEY",     "SUPPLIER", "SUPPKEY"),
        ("SUPPLIER", "NATIONKEY", "CUSTOMER", "NATIONKEY"),
    ]


    schema_2 = {
        "LINEITEM": ["O_KEY", "PARTKEY", "S_KEY", "L_QUANTITY"],
        "SUPPLIER": ["SUPPKEY", "NATIONKEY", "S_NAME"],
        "CUSTOMER": ["CUSTKEY", "NATIONKEY", "C_NAME"],
    }

    tables_2 = ["LINEITEM", "SUPPLIER", "CUSTOMER"]

    joins_2 = [
        ("LINEITEM", "S_KEY",     "SUPPLIER", "SUPPKEY"),
        ("SUPPLIER", "NATIONKEY", "CUSTOMER", "NATIONKEY"),
    ]

    col_to_var, var_to_col, edges = build_hypergraph(schema_2, tables_2, joins_2)

    print("=== col_to_var: (table, col) -> canonical vertex name ===")
    for (table, col), canon in col_to_var.items():
        print(f"  ({table}, {col}) -> {canon}")

    print("\n=== var_to_col: (table, canonical) -> actual column in that table ===")
    for (table, canon), col in var_to_col.items():
        print(f"  ({table}, {canon}) -> {col}")

    print("\n=== hyperedges (one per table) ===")
    print(edges)
