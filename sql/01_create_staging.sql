-- Staging layer: raw data lands here as-is, minimal transformation.
-- Mirrors the shape of the source CSV so loading is a straight copy.

CREATE TABLE IF NOT EXISTS staging_sales (
    order_id        VARCHAR(20),
    order_date      DATE,
    customer_id     VARCHAR(20),
    customer_name   VARCHAR(100),
    customer_email  VARCHAR(150),
    customer_city   VARCHAR(100),
    customer_state  VARCHAR(50),
    product_id      VARCHAR(20),
    product_name    VARCHAR(150),
    product_category VARCHAR(100),
    unit_price      DECIMAL(10, 2),
    quantity        INT,
    store_id        VARCHAR(20),
    store_name      VARCHAR(100),
    store_region    VARCHAR(50)
);
