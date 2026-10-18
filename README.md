# Retail Sales Data Warehouse

A basic data warehousing project: a star-schema warehouse in MySQL, loaded from
synthetic retail sales data via a Python ETL pipeline.

## Architecture

```
data/raw_sales.csv  --extract-->  staging_sales  --transform-->  dim_* / fact_sales
   (source system)                 (staging layer)                (star schema)
```

- **Staging layer** (`staging_sales`): raw data landed as-is from the source CSV.
- **Warehouse layer** (star schema):
  - `fact_sales` — one row per order line item (quantity, unit price, total amount)
  - `dim_date`, `dim_customer`, `dim_product`, `dim_store` — conformed dimensions with surrogate keys

## Prerequisites

- Docker (for MySQL) — or point `.env` at an existing MySQL instance
- Python 3.10+

## Setup

```bash
cp .env.example .env
docker compose up -d
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

## Run the pipeline

```bash
cd etl
python run_pipeline.py
```

This generates ~3,000 synthetic orders (`data/raw_sales.csv`), creates the schema,
loads staging, then transforms and loads the star schema. Steps can also be run
individually:

```bash
python generate_sample_data.py     # source data
python create_schema.py            # DDL: staging + warehouse tables
python extract_load_staging.py     # extract & load staging
python transform_load_warehouse.py # transform & load star schema
```

## Explore the data

Connect with any MySQL client (host `127.0.0.1`, port `3307`, credentials from `.env`)
and try the queries in [sql/03_example_queries.sql](sql/03_example_queries.sql) — monthly
revenue, top products, revenue by region, top customers, weekday vs. weekend sales.

```bash
docker exec -it retail_dw_mysql mysql -u dw_user -p retail_dw
```

## Project layout

```
sql/
  01_create_staging.sql    staging table DDL
  02_create_warehouse.sql  star schema DDL (dims + fact, with FKs and indexes)
  03_example_queries.sql   sample analytical queries
etl/
  generate_sample_data.py     creates the synthetic source CSV
  create_schema.py            runs the DDL scripts
  extract_load_staging.py     CSV -> staging_sales
  transform_load_warehouse.py staging -> dims + fact
  run_pipeline.py             runs all steps in order
data/
  raw_sales.csv             generated source data (gitignored)
```

## Notes

- The Docker container publishes MySQL on host port **3307** (not the default 3306),
  because this machine already has another MySQL server running locally on 3306.
  If that's not an issue on your machine, feel free to change `MYSQL_PORT` in `.env`
  back to 3306.

- The pipeline uses a **full-refresh** pattern (truncate + reload) — simplest
  option for a basic project. A production warehouse would typically load
  incrementally and track slowly changing dimensions (SCD Type 1/2).
- `dim_date` is pre-populated for 2020–2030 regardless of the source data range,
  which is standard practice for a date dimension.
