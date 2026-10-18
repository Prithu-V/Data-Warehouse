-- Star schema: one fact table (sales) surrounded by conformed dimensions.
-- Surrogate keys (INT AUTO_INCREMENT) decouple the warehouse from source
-- system IDs so dimensions can evolve (SCD) without touching the fact table.

CREATE TABLE IF NOT EXISTS dim_date (
    date_key        INT PRIMARY KEY,        -- YYYYMMDD
    full_date       DATE NOT NULL,
    day             INT NOT NULL,
    month           INT NOT NULL,
    month_name      VARCHAR(10) NOT NULL,
    quarter         INT NOT NULL,
    year            INT NOT NULL,
    day_of_week     VARCHAR(10) NOT NULL,
    is_weekend      BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key    INT AUTO_INCREMENT PRIMARY KEY,
    customer_id     VARCHAR(20) NOT NULL UNIQUE,
    customer_name   VARCHAR(100) NOT NULL,
    email           VARCHAR(150),
    city            VARCHAR(100),
    state           VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key     INT AUTO_INCREMENT PRIMARY KEY,
    product_id      VARCHAR(20) NOT NULL UNIQUE,
    product_name    VARCHAR(150) NOT NULL,
    category        VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_store (
    store_key       INT AUTO_INCREMENT PRIMARY KEY,
    store_id        VARCHAR(20) NOT NULL UNIQUE,
    store_name      VARCHAR(100) NOT NULL,
    region          VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fact_sales (
    sales_key       BIGINT AUTO_INCREMENT PRIMARY KEY,
    order_id        VARCHAR(20) NOT NULL,
    date_key        INT NOT NULL,
    customer_key    INT NOT NULL,
    product_key     INT NOT NULL,
    store_key       INT NOT NULL,
    quantity        INT NOT NULL,
    unit_price      DECIMAL(10, 2) NOT NULL,
    total_amount    DECIMAL(12, 2) NOT NULL,
    FOREIGN KEY (date_key)     REFERENCES dim_date(date_key),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (product_key)  REFERENCES dim_product(product_key),
    FOREIGN KEY (store_key)    REFERENCES dim_store(store_key)
);

CREATE INDEX idx_fact_sales_date     ON fact_sales(date_key);
CREATE INDEX idx_fact_sales_customer ON fact_sales(customer_key);
CREATE INDEX idx_fact_sales_product  ON fact_sales(product_key);
CREATE INDEX idx_fact_sales_store    ON fact_sales(store_key);
