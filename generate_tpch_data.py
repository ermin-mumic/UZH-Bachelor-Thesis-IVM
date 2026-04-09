import argparse
import os
import duckdb


TPCH_TABLES = [
    "customer",
    "orders",
    "lineitem",
    "partsupp",
    "part",
    "supplier",
    "nation",
    "region",
]


def parse_args():
    parser = argparse.ArgumentParser(description="Generate tpch data.")
    parser.add_argument(
        "--sf",
        type=float,
        default=1.0,
        help="TPC-H scale factor (e.g., 0.1, 1, 10).",
    )
    parser.add_argument(
        "--output-dir",
        default="data",
        help="Directory where CSV files will be written.",
    )
    return parser.parse_args()


def generate_tpch_csvs(sf: float, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    con = duckdb.connect(database=":memory:")
    con.execute("INSTALL tpch;")
    con.execute("LOAD tpch;")
    con.execute(f"CALL dbgen(sf={sf});")

    for table in TPCH_TABLES:
        out_path = os.path.join(output_dir, f"{table}.csv")
        con.execute(
            f"COPY {table} TO '{out_path}' (FORMAT CSV, HEADER);"
        )
        print(f"Wrote {out_path}")

    con.close()


if __name__ == "__main__":
    args = parse_args()

    generate_tpch_csvs(sf=args.sf, output_dir=args.output_dir)

    print("\nTPC-H CSV generation complete.")
    print(f"Scale factor: {args.sf}")
    print(f"Output directory: {args.output_dir}")
