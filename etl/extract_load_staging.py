"""Extract: reads the raw CSV and loads it verbatim into staging_sales."""

from pathlib import Path

import pandas as pd
from db import get_connection

CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_sales.csv"

INSERT_SQL = """
    INSERT INTO staging_sales (
        order_id, order_date, customer_id, customer_name, customer_email,
        customer_city, customer_state, product_id, product_name,
        product_category, unit_price, quantity, store_id, store_name, store_region
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


def main():
    df = pd.read_csv(CSV_PATH)
    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]

    conn = get_connection()
    cursor = conn.cursor()
    try:
        print("Truncating staging_sales ...")
        cursor.execute("TRUNCATE TABLE staging_sales")
        print(f"Loading {len(rows)} rows into staging_sales ...")
        cursor.executemany(INSERT_SQL, rows)
        conn.commit()
        print("Staging load complete.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
