-- Example analytical queries against the star schema.

-- Total revenue by month
SELECT d.year, d.month_name, ROUND(SUM(f.total_amount), 2) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;

-- Top 10 products by revenue
SELECT p.product_name, p.category, ROUND(SUM(f.total_amount), 2) AS revenue
FROM fact_sales f
JOIN dim_product p ON f.product_key = p.product_key
GROUP BY p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- Revenue by store region
SELECT s.region, ROUND(SUM(f.total_amount), 2) AS revenue, COUNT(DISTINCT f.order_id) AS orders
FROM fact_sales f
JOIN dim_store s ON f.store_key = s.store_key
GROUP BY s.region
ORDER BY revenue DESC;

-- Top 10 customers by total spend
SELECT c.customer_name, c.state, ROUND(SUM(f.total_amount), 2) AS total_spent
FROM fact_sales f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.customer_name, c.state
ORDER BY total_spent DESC
LIMIT 10;

-- Weekday vs weekend sales
SELECT d.is_weekend, ROUND(SUM(f.total_amount), 2) AS revenue, COUNT(*) AS line_items
FROM fact_sales f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.is_weekend;
