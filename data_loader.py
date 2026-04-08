import pandas as pd


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

def prepare_data(table_names: list, csv_dir: str = '.', batch_size: int = 1) -> list:

    tables = {}

    print("Loading CSV files.")
    for table_name in table_names:
        csv_file = f"{csv_dir}/{table_name.lower()}.csv"
        df = pd.read_csv(csv_file)
        df.columns = df.columns.str.upper()

        rename_map = JOIN_KEY_RENAME_MAP.get(table_name.upper(), {})
        if rename_map:
            df = df.rename(columns=rename_map)

        tables[table_name] = df
        print(f" {table_name}: {len(df)} rows")
    
    insert_sequence = []

    current_row = {name: 0 for name in table_names}

    while True:
        added_any = False

        for table_name in table_names:
            df = tables[table_name]
            start = current_row[table_name]

            if start >= len(df):
                continue

            end = min(start + batch_size, len(df))
            batch_df = df.iloc[start:end]

            insert_sequence.append((table_name, batch_df))
            current_row[table_name] = end
            added_any = True
        
        if not added_any:
            break
                
    return insert_sequence
