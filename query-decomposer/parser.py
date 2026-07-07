import sqlglot
import sqlglot.expressions as exp
from sqlglot.errors import ParseError


def parse_schema(sql):
    try:
        statements = sqlglot.parse(sql)
    except ParseError as e:
        raise ValueError(f"Invalid SQL syntax in table definitions:\n{e}") from e

    schema = {}

    for stmt in statements:

        if not isinstance(stmt, exp.Create):
            continue

        schema_node = stmt.this
        table_name = schema_node.this.name.upper()

        columns = []

        for item in schema_node.expressions:
            if isinstance(item, exp.ColumnDef):
                columns.append(item.name.upper())

        schema[table_name] = columns

    if not schema:
        raise ValueError("No CREATE TABLE statements found. ")

    return schema

# User must verify semantics etc in a database engine
def parse_query(sql, schema):
    try:
        ast = sqlglot.parse_one(sql)
    except ParseError as e:
        raise ValueError(f"Invalid SQL syntax in query:\n{e}") from e


    tables = []          # alias names of tables in query order (alias = physical name when no alias)
    alias_to_table = {}  # alias → physical table name (also physical → physical for bare tables)
    joins = []           # join conditions as 4 tuples e.g. ("Table1", "JOIN Attribute1", "Table2", "JOIN Attribute2")
    predicates = {}      # alias → list of SQL strings e.g. {"R1": ["A > 5"]}
    combined_schema = dict(schema)  # schema extended with alias entries so hypergraph can find their variables (self joins)

    def register_table(tbl_node):
        name = tbl_node.name.upper()
        alias = (tbl_node.alias or tbl_node.name).upper()

        if name not in schema:
            raise ValueError(f"Table {name} is not defined.")

        # extract column rename list from AS alias(col1, col2, ...)
        alias_node = tbl_node.args.get("alias")
        col_list = []
        if alias_node:
            col_list = [c.name.upper() for c in (alias_node.args.get("columns") or [])]

        # if aliased table
        if alias != name:
            # use explicit col list if given, otherwise copy physical schema columns
            combined_schema[alias] = col_list if col_list else list(schema[name])

        tables.append(alias)
        alias_to_table[alias] = name
        alias_to_table[name] = name

    # -- SELECT CLAUSE --
    # allow CREATE VIEW ... AS SELECT or just SELECT
    if isinstance(ast, exp.Create):
        ast = ast.find(exp.Select)
        if not ast:
            raise ValueError("Could not find a SELECT statement inside the CREATE VIEW.")
    if not isinstance(ast, exp.Select):
        raise ValueError("Query must be a SELECT statement.")

    exprs = ast.args.get("expressions") or []
    if len(exprs) != 1 or not isinstance(exprs[0], exp.Star):
        raise ValueError("Query must use SELECT * (full conjunctive query).")
    
    # -- FROM CLAUSE -- (must have only 1 table)
    from_node = ast.find(exp.From)
    if not from_node:
        raise ValueError("Query has no FROM clause.")
    tbl = from_node.find(exp.Table)
    register_table(tbl)

    def resolve_table_ref(ref):
        # Resolve a table reference (alias or physical name) in a join to the alias identifier in tables. Edge case: FROM EDGES AS R1... JOIN ON EDGES.B 
        ref = ref.upper()
        if ref in tables:
            return ref
        matches = [a for a, phys in alias_to_table.items() if phys == ref and a in tables]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            raise ValueError(f"Ambiguous table reference '{ref}' — multiple aliases exist for this table. Use the alias directly.")
        else:
            raise ValueError(f"Unknown table reference '{ref}'.")

    # -- JOIN CLAUSES --
    for join in ast.args.get("joins") or []:

        tbl = join.find(exp.Table)
        if not tbl:
            continue

        register_table(tbl)
        tbl_alias = (tbl.alias or tbl.name).upper()        # alias identifier (= physical name when no alias)

        # --- Case 1: JOIN ... USING (col) ---
        # join.args["using"] is a list of Identifier nodes, one per column named
        for col in join.args.get("using") or []:
            col_name = col.name.upper()

            if col_name not in combined_schema[tbl_alias]:
                raise ValueError(f"Table {tbl_alias} has no column {col_name}.")

            found = False
            for prev_tbl in tables[:-1]:
                if col_name in combined_schema.get(prev_tbl, []):
                    joins.append((prev_tbl, col_name, tbl_alias, col_name))
                    found = True

            if not found:
                raise ValueError(f"Column {col_name} used in JOIN USING not found in any previous table.")

        # --- Case 2: JOIN ... ON left.col = right.col ---
        # join.args["on"] is an expression tree, find_all(EQ) walks it for equality conditions
        on_node = join.args.get("on")
        for eq in (on_node.find_all(exp.EQ) if on_node else []):
            left_col  = eq.left
            right_col = eq.right
            if isinstance(left_col, exp.Column) and isinstance(right_col, exp.Column):
                lt = resolve_table_ref(left_col.table.upper())
                rt = resolve_table_ref(right_col.table.upper())
                joins.append((lt, left_col.name.upper(), rt, right_col.name.upper()))

    # -- WHERE CLAUSE --
    def split_and(expr):
        if isinstance(expr, exp.And):
            return split_and(expr.left) + split_and(expr.right)
        return [expr]

    where_node = ast.args.get("where")
    if where_node:
        for cond in split_and(where_node.this):
            cols = list(cond.find_all(exp.Column))

            # find which table(s) this condition touches
            tables_in_cond = set()
            for col in cols:
                if col.table:
                    tables_in_cond.add(resolve_table_ref(col.table.upper()))
                else:
                    # unqualified column: find owner from combined_schema
                    owners = [t for t in tables if col.name.upper() in combined_schema.get(t, [])]
                    if len(owners) == 1:
                        tables_in_cond.add(owners[0])
                    elif len(owners) > 1:
                        raise ValueError(
                            f"Ambiguous column '{col.name}' in WHERE — qualify it with a table name."
                        )

            if len(tables_in_cond) == 0:
                continue  # constant like WHERE 1=1, ignore

            if len(tables_in_cond) > 1:
                raise ValueError(
                    f"WHERE condition spans multiple tables, which is not supported: {cond.sql()}"
                )

            tbl = next(iter(tables_in_cond)) # extract that 1 table

            # build column → physical col mapping for this table/alias
            phys_table  = alias_to_table.get(tbl, tbl)
            var_names   = combined_schema[tbl]
            phys_cols   = combined_schema[phys_table]
            var_to_phys = {var: phys_cols[i] for i, var in enumerate(var_names) if i < len(phys_cols)}

            # walk node and apply lambda: strip table qualifiers AND map column names to physical cols
            # e.g. R1.A > 5  →  SRC > 5  (for EDGES AS R1(A, B) where EDGES has [SRC, DST])
            # for regular tables var_to_phys is identity so predicate is unchanged
            clean = cond.transform(
                lambda node: exp.column(var_to_phys.get(node.name.upper(), node.name))
                             if isinstance(node, exp.Column) else node
            )
            predicates.setdefault(tbl, []).append(clean.sql()) # inserts key if it doesnt exist yet with default value []

    return tables, alias_to_table, joins, predicates, combined_schema


if __name__ == "__main__":

    schema_sql_1 = """
        CREATE TABLE LINEITEM (
            ORDERKEY  bigint not null,
            PARTKEY   bigint not null,
            SUPPKEY   bigint not null,
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

    query_sql_1 = """
        SELECT * FROM LINEITEM
        JOIN SUPPLIER USING (SUPPKEY)
        JOIN CUSTOMER USING (NATIONKEY)
    """

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

    schema_sql_3 = """
        -- The TPC-H Schema.
CREATE TABLE PART (
    PARTKEY bigint not null,
    P_NAME varchar(55),
    P_MFGR char(25),
    P_BRAND char(10),
    P_TYPE varchar(25),
    P_SIZE integer,
    P_CONTAINER char(10),
    P_RETAILPRICE decimal(12,2),
    P_COMMENT varchar(23),
    PRIMARY KEY (PARTKEY)
) WITH ('materialized' = 'true');

CREATE TABLE SUPPLIER (
    SUPPKEY bigint not null,
    S_NAME char(25),
    S_ADDRESS varchar(40),
    NATIONKEY bigint not null,
    S_PHONE char(15),
    S_ACCTBAL decimal(12,2),
    S_COMMENT varchar(101),
    PRIMARY KEY (SUPPKEY)
) WITH ('materialized' = 'true');

CREATE TABLE PARTSUPP (
    PARTKEY bigint not null,
    SUPPKEY bigint not null,
    PS_AVAILQTY integer,
    PS_SUPPLYCOST decimal(12,2),
    PS_COMMENT varchar(199),
    PRIMARY KEY (PARTKEY, SUPPKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/partsupp.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE CUSTOMER (
    CUSTKEY bigint not null,
    C_NAME varchar(25),
    C_ADDRESS varchar(40),
    NATIONKEY bigint not null,
    C_PHONE char(15),
    C_ACCTBAL decimal(12,2),
    C_MKTSEGMENT char(10),
    C_COMMENT varchar(117),
    PRIMARY KEY (CUSTKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/customer.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE ORDERS (
    ORDERKEY bigint not null,
    CUSTKEY bigint not null,
    O_ORDERSTATUS char(1),
    O_TOTALPRICE decimal(12,2),
    O_ORDERDATE date,
    O_ORDERPRIORITY char(15),
    O_CLERK char(15),
    O_SHIPPRIORITY integer,
    O_COMMENT varchar(79),
    PRIMARY KEY (ORDERKEY)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/orders.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE LINEITEM (
    ORDERKEY bigint not null,
    PARTKEY bigint not null,
    SUPPKEY bigint not null,
    L_LINENUMBER integer not null,
    L_QUANTITY decimal(12,2),
    L_EXTENDEDPRICE decimal(12,2),
    L_DISCOUNT decimal(12,2),
    L_TAX decimal(12,2),
    L_RETURNFLAG char(1),
    L_LINESTATUS char(1),
    L_SHIPDATE date,
    L_COMMITDATE date,
    L_RECEIPTDATE date,
    L_SHIPINSTRUCT char(25),
    L_SHIPMODE char(10),
    L_COMMENT varchar(44),
    PRIMARY KEY (ORDERKEY, L_LINENUMBER)
) WITH (
    'connectors' = '[{
        "transport": {
            "name": "file_input",
            "config": {
                "path": "/{{FILE_PATH}}/lineitem.csv"
            }
        },
        "format": { 
            "name": "csv",
            "config": {
                "headers": true
            }
        }
    }]'
);

CREATE TABLE NATION (
    NATIONKEY bigint not null,
    N_NAME char(25),
    REGIONKEY bigint not null,
    N_COMMENT varchar(152),
    PRIMARY KEY (NATIONKEY)
) WITH ('materialized' = 'true');

CREATE TABLE REGION (
    REGIONKEY bigint not null,
    R_NAME char(25),
    R_COMMENT varchar(152),
    PRIMARY KEY (REGIONKEY)
) WITH ('materialized' = 'true');
    """

    query_sql_3 = """
        SELECT *
        FROM LINEITEM
        JOIN ORDERS USING (ORDERKEY)
        JOIN CUSTOMER USING (CUSTKEY)
        JOIN PARTSUPP USING (PARTKEY, SUPPKEY);
    """

    schema = parse_schema(schema_sql_3)
    print("=== Schema ===")
    for table, cols in schema.items():
        print(f"  {table}: {cols}")

    tables, alias_to_table, joins, predicates, combined_schema = parse_query(query_sql_3, schema)
    print("\n=== Query ===")
    print(f" Tables used: {tables}")
    print(f" Join conditions:")
    for j in joins:
        print(f"    {j[0]}.{j[1]}  =  {j[2]}.{j[3]}")
    print("\n=== Mapping ===")
    print(f"  Alias Table Mappings:\n{alias_to_table}")
