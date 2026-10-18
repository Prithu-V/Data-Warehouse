"""Runs the DDL scripts in sql/ against the target database, in order."""

from pathlib import Path

import mysql.connector
from db import get_connection

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"
DDL_FILES = ["01_create_staging.sql", "02_create_warehouse.sql"]

# MySQL has no `CREATE INDEX IF NOT EXISTS`, so re-running the DDL on an
# already-provisioned database hits "duplicate key name" (1061) — safe to skip.
ER_DUP_KEYNAME = 1061


def run_sql_file(cursor, path: Path):
    statements = path.read_text().split(";")
    for statement in statements:
        statement = statement.strip()
        if statement:
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                if e.errno == ER_DUP_KEYNAME:
                    continue
                raise


def main():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for filename in DDL_FILES:
            print(f"Running {filename} ...")
            run_sql_file(cursor, SQL_DIR / filename)
        conn.commit()
        print("Schema created.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
