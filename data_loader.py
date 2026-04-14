import pandas as pd
import duckdb
import os
import math


JOIN_KEY_RENAME_MAP = {
    "CUSTOMER": {
        "C_CUSTKEY": "CUSTKEY",
        "C_NATIONKEY": "NATIONKEY"
    },
    "SUPPLIER":{
        "S_SUPPKEY": "SUPPKEY",
        "S_NATIONKEY": "NATIONKEY"
    },
    "PART": {
        "P_PARTKEY": "PARTKEY",
    },
    "NATION": {
        "N_NATIONKEY": "NATIONKEY",
        "N_REGIONKEY": "REGIONKEY"
    },
    "REGION": {
        "R_REGIONKEY": "REGIONKEY"
    },
    "ORDERS": {
        "O_ORDERKEY": "ORDERKEY",
        "O_CUSTKEY": "CUSTKEY",
    },
    "LINEITEM": {
        "L_ORDERKEY": "ORDERKEY",
        "L_PARTKEY": "PARTKEY",
        "L_SUPPKEY": "SUPPKEY",
    },
    "PARTSUPP": {
        "PS_PARTKEY": "PARTKEY",
        "PS_SUPPKEY": "SUPPKEY",
    },
}

def prepare_data_generator(table_names: list, csv_dir: str = '.', batch_size: int = 1):
    
    table_names = [t.upper() for t in table_names]
    con = duckdb.connect(database=":memory:")
    total_rows_to_be_inserted = 0
    row_counts = {}

    print("Mapping and Renaming CSV files.\n")
    for table_name in table_names:
        csv_file = os.path.join(csv_dir, f"{table_name.lower()}.csv")

        table_renames = JOIN_KEY_RENAME_MAP.get(table_name, {})
        columns_info = con.execute(f"DESCRIBE SELECT * FROM read_csv_auto('{csv_file}')").fetchall()

        select_items = []
        for col in columns_info:
            old_name = col[0]
            old_name_upper = old_name.upper()

            new_name = table_renames.get(old_name_upper, old_name_upper)

            if "DATE" in old_name_upper:
                sql_col = f'CAST ("{old_name}" AS VARCHAR) AS {new_name}'
            else:
                sql_col = f'"{old_name}" AS {new_name}'

            select_items.append(sql_col)
        
        select_clause = ", ".join(select_items)

        con.execute(f"""
            CREATE VIEW {table_name}_raw AS 
            SELECT {select_clause}
            FROM read_csv_auto('{csv_file}')  
        """)

        count = con.execute(f"SELECT count(*) FROM {table_name}_raw").fetchone()[0]
        row_counts[table_name] = count
        total_rows_to_be_inserted += count

        print(f" {table_name}: {count} rows mapped.")

    offsets = {t: 0 for t in table_names}

    yield {"total_rows": total_rows_to_be_inserted, "total_batches": math.ceil(total_rows_to_be_inserted/batch_size)}

    while any(offsets[t]<row_counts[t] for t in table_names):
        for table_name in table_names:
            start = offsets[table_name]
            total = row_counts[table_name]

            if start >= total:
                continue

            query = f"SELECT * FROM {table_name}_raw LIMIT {batch_size} OFFSET {start}"
            batch_df = con.execute(query).df()

            # Convert batch dataframe to JSON array of objects representing rows
            # --> '[{"col1":1, "col2":"a"},{"col1":2, "col2":"b"}]' as feldera requires json_flavor = pandas
            json_str = batch_df.to_json(orient="records")

            yield (table_name, json_str)

            offsets[table_name] += batch_size


    con.close()

            