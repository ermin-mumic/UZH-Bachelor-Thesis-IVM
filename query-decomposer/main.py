from parser import parse_schema, parse_query
from hypergraph import build_hypergraph
from htd_runner import run_htd
from sql_generator import generate_sql


def run_pipeline(schema_sql, query_sql):
    # parse → hypergraph → htd
    # returns all intermediate data needed for sql generation
    schema = parse_schema(schema_sql)
    tables, _, joins, predicates = parse_query(query_sql, schema)
    _, var_to_col, edges = build_hypergraph(schema, tables, joins)
    bags, tree_edges, treewidth = run_htd(edges, tables)
    return tables, edges, var_to_col, bags, tree_edges, treewidth, predicates


def generate(tables, edges, var_to_col, bags, tree_edges, predicates, root):
    # reruns sql generation with a different root
    return generate_sql(tables, edges, var_to_col, bags, tree_edges, predicates, root)


if __name__ == "__main__":
    schema_sql_2 = """
        CREATE TABLE LINEITEM (
            O_Key  bigint not null,
            PARTKEY   bigint not null,
            S_KEY   bigint not null,
            L_QUANTITY decimal(12,2),
            PRIMARY KEY (ORDERKEY)
        );

        CREATE TABLE SUPPLIER (
            SUPPKEY   bigint not null,
            NATIONKEY bigint not null,
            S_NAME    char(25),
            PRIMARY KEY (SUPPKEY)
        );

        CREATE TABLE CUSTOMER (
            CUSTKEY   bigint not null,
            NATIONKEY bigint not null,
            C_NAME    varchar(25),
            PRIMARY KEY (CUSTKEY)
        );
    """

    query_sql_2 = """
        SELECT * FROM LINEITEM L
        JOIN SUPPLIER S ON L.S_KEY = S.SUPPKEY
        JOIN CUSTOMER USING (NATIONKEY)
    """

    tables, edges, var_to_col, bags, tree_edges, treewidth, predicates = run_pipeline(schema_sql_2, query_sql_2)
    views = generate(tables, edges, var_to_col, bags, tree_edges, predicates, root=1)

    print(f"-- Treewidth: {treewidth}")
    print()
    for view_sql in views:
        print(view_sql)
        print()
