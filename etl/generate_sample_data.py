"""Generates a synthetic retail sales CSV to act as the warehouse's source system extract."""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_sales.csv"

NUM_CUSTOMERS = 200
NUM_PRODUCTS = 60
NUM_STORES = 8
NUM_ORDERS = 3000
START_DATE = date(2025, 1, 1)
END_DATE = date(2025, 12, 31)

CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Sporting Goods", "Books", "Toys"]
REGIONS = ["North", "South", "East", "West", "Central"]


def build_customers():
    return [
        {
            "customer_id": f"C{str(i).zfill(4)}",
            "customer_name": fake.name(),
            "customer_email": fake.email(),
            "customer_city": fake.city(),
            "customer_state": fake.state_abbr(),
        }
        for i in range(1, NUM_CUSTOMERS + 1)
    ]


def build_products():
    return [
        {
            "product_id": f"P{str(i).zfill(4)}",
            "product_name": f"{fake.word().capitalize()} {random.choice(['Pro', 'Max', 'Lite', 'Plus', 'Basic'])}",
            "product_category": random.choice(CATEGORIES),
            "unit_price": round(random.uniform(5, 500), 2),
        }
        for i in range(1, NUM_PRODUCTS + 1)
    ]


def build_stores():
    return [
        {
            "store_id": f"S{str(i).zfill(3)}",
            "store_name": f"{fake.city()} Store",
            "store_region": random.choice(REGIONS),
        }
        for i in range(1, NUM_STORES + 1)
    ]


def random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def main():
    customers = build_customers()
    products = build_products()
    stores = build_stores()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "order_id", "order_date", "customer_id", "customer_name", "customer_email",
                "customer_city", "customer_state", "product_id", "product_name",
                "product_category", "unit_price", "quantity", "store_id", "store_name",
                "store_region",
            ]
        )

        for order_num in range(1, NUM_ORDERS + 1):
            order_id = f"O{str(order_num).zfill(6)}"
            order_date = random_date(START_DATE, END_DATE)
            customer = random.choice(customers)
            store = random.choice(stores)

            # each order has 1-4 line items (products)
            for product in random.sample(products, k=random.randint(1, 4)):
                writer.writerow(
                    [
                        order_id,
                        order_date.isoformat(),
                        customer["customer_id"],
                        customer["customer_name"],
                        customer["customer_email"],
                        customer["customer_city"],
                        customer["customer_state"],
                        product["product_id"],
                        product["product_name"],
                        product["product_category"],
                        product["unit_price"],
                        random.randint(1, 5),
                        store["store_id"],
                        store["store_name"],
                        store["store_region"],
                    ]
                )

    print(f"Wrote sample data to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
