"""Transform + Load: populates dimension tables and the fact table from staging.

Uses a full-refresh pattern (truncate + reload) since this is a small batch
warehouse — good enough for a basic project, not meant for incremental/CDC loads.
"""

from datetime import date, timedelta

from db import get_connection

DIM_DATE_START = date(2020, 1, 1)
DIM_DATE_END = date(2030, 12, 31)

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def load_dim_date(cursor):
    print("Populating dim_date ...")
    cursor.execute("TRUNCATE TABLE dim_date")
    rows = []
    current = DIM_DATE_START
    while current <= DIM_DATE_END:
        date_key = int(current.strftime("%Y%m%d"))
        quarter = (current.month - 1) // 3 + 1
        weekday = current.weekday()  # 0 = Monday
        rows.append(
            (
                date_key, current, current.day, current.month, MONTH_NAMES[current.month - 1],
                quarter, current.year, DAY_NAMES[weekday], weekday >= 5,
            )
        )
        current += timedelta(days=1)

    cursor.executemany(
        """INSERT INTO dim_date
           (date_key, full_date, day, month, month_name, quarter, year, day_of_week, is_weekend)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        rows,
    )


def load_dim_customer(cursor):
    print("Populating dim_customer ...")
    cursor.execute(
        """INSERT INTO dim_customer (customer_id, customer_name, email, city, state)
           SELECT DISTINCT customer_id, customer_name, customer_email, customer_city, customer_state
           FROM staging_sales
           ON DUPLICATE KEY UPDATE
               customer_name = VALUES(customer_name),
               email = VALUES(email),
               city = VALUES(city),
               state = VALUES(state)"""
    )


def load_dim_product(cursor):
    print("Populating dim_product ...")
    cursor.execute(
        """INSERT INTO dim_product (product_id, product_name, category)
           SELECT DISTINCT product_id, product_name, product_category
           FROM staging_sales
           ON DUPLICATE KEY UPDATE
               product_name = VALUES(product_name),
               category = VALUES(category)"""
    )


def load_dim_store(cursor):
    print("Populating dim_store ...")
    cursor.execute(
        """INSERT INTO dim_store (store_id, store_name, region)
           SELECT DISTINCT store_id, store_name, store_region
           FROM staging_sales
           ON DUPLICATE KEY UPDATE
               store_name = VALUES(store_name),
               region = VALUES(region)"""
    )


def load_fact_sales(cursor):
    print("Populating fact_sales ...")
    cursor.execute(
        """INSERT INTO fact_sales
               (order_id, date_key, customer_key, product_key, store_key,
                quantity, unit_price, total_amount)
           SELECT
               s.order_id,
               CAST(DATE_FORMAT(s.order_date, '%Y%m%d') AS UNSIGNED),
               c.customer_key,
               p.product_key,
               st.store_key,
               s.quantity,
               s.unit_price,
               s.quantity * s.unit_price
           FROM staging_sales s
           JOIN dim_customer c ON c.customer_id = s.customer_id
           JOIN dim_product p  ON p.product_id = s.product_id
           JOIN dim_store st   ON st.store_id = s.store_id"""
    )


def main():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # TRUNCATE on dim_date/fact_sales ignores row counts and just checks for
        # FK relationships, so referential checks must be relaxed for the reload.
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        print("Truncating fact_sales ...")
        cursor.execute("TRUNCATE TABLE fact_sales")
        load_dim_date(cursor)
        load_dim_customer(cursor)
        load_dim_product(cursor)
        load_dim_store(cursor)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        load_fact_sales(cursor)
        conn.commit()
        print("Warehouse load complete.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
