
-- ------------------
-- a) KPI Metrics
-- ------------------


-- 1. Total Revenue

SELECT ROUND(SUM(revenue),2) AS total_revenue
FROM sales_fact;


-- 2. Total Orders

SELECT COUNT(*) AS total_orders
FROM sales_fact;


-- 3. Total Quantity Sold

SELECT SUM(quantity) AS total_items_sold
FROM sales_fact;


-- 4. Unique Customers

SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM sales_fact;


-- 5. Unique Products Sold

SELECT COUNT(DISTINCT product_id) AS unique_products
FROM sales_fact;



-- ---------------------------
-- b) Time-Based Analytics
-- ---------------------------


-- 6. Monthly Revenue Trend

SELECT year, month, SUM(revenue) AS monthly_revenue
FROM sales_fact
JOIN date_dimension USING(date_id)
GROUP BY year, month
ORDER BY year, month;


-- 7. Monthly Quantity Sold

SELECT year, month, SUM(quantity) AS monthly_quantity
FROM sales_fact
JOIN date_dimension USING(date_id)
GROUP BY year, month
ORDER BY year, month;


-- 8. Daily Sales

SELECT date, SUM(revenue) AS daily_sales
FROM sales_fact
JOIN date_dimension USING(date_id)
GROUP BY date
ORDER BY date;


-- 9. Revenue by Year

SELECT year, SUM(revenue) AS yearly_revenue
FROM sales_fact
JOIN date_dimension USING(date_id)
GROUP BY year;


-- 10. Average Daily Revenue

SELECT AVG(daily_revenue)
FROM (
    SELECT date, SUM(revenue) AS daily_revenue
    FROM sales_fact
    JOIN date_dimension USING(date_id)
    GROUP BY date
) AS daily_sales;



-- ----------------------------
-- c) Product Analytics
-- ----------------------------


-- 11. Top 10 Products by Revenue

SELECT product_name, SUM(revenue) AS total_revenue
FROM sales_fact
JOIN product_dimension USING(product_id)
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 12. Top 10 Products by Quantity

SELECT product_name, SUM(quantity) AS total_quantity
FROM sales_fact
JOIN product_dimension USING(product_id)
GROUP BY product_name
ORDER BY total_quantity DESC
LIMIT 10;


-- 13. Least Selling Products

SELECT product_name, SUM(quantity) AS total_quantity
FROM sales_fact
JOIN product_dimension USING(product_id)
GROUP BY product_name
ORDER BY total_quantity ASC
LIMIT 10;


-- 14. Average Revenue per Product

SELECT product_name, AVG(revenue) AS avg_revenue
FROM sales_fact
JOIN product_dimension USING(product_id)
GROUP BY product_name
ORDER BY avg_revenue DESC
LIMIT 10;


-- 15. Products Generating Revenue Above Average

SELECT product_name, SUM(revenue) AS total_revenue
FROM sales_fact
JOIN product_dimension USING(product_id)
GROUP BY product_name
HAVING total_revenue > (
    SELECT AVG(revenue) FROM sales_fact
);



-- ---------------------------
-- d) Customer Analytics
-- ---------------------------


-- 16. Top 10 Customers by Revenue

SELECT customer_id, SUM(revenue) AS total_spent
FROM sales_fact
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;


-- 17. Average Spending per Customer

SELECT AVG(customer_spending)
FROM (
    SELECT customer_id, SUM(revenue) AS customer_spending
    FROM sales_fact
    GROUP BY customer_id
) AS customer_totals;


-- 18. Customers With Highest Purchase Quantity

SELECT customer_id, SUM(quantity) AS total_items
FROM sales_fact
GROUP BY customer_id
ORDER BY total_items DESC
LIMIT 10;


-- 19. Customers With More Than 50 Purchases

SELECT customer_id, COUNT(*) AS purchase_count
FROM sales_fact
GROUP BY customer_id
HAVING purchase_count > 50;


-- 20. Customer Revenue Distribution

SELECT customer_id, SUM(revenue) AS total_spent
FROM sales_fact
GROUP BY customer_id
ORDER BY total_spent DESC;



-- ----------------------------
-- e) Geographic Analytics
-- ----------------------------


-- 21. Revenue by Country

SELECT country, SUM(revenue) AS total_revenue
FROM sales_fact
JOIN customer_dimension USING(customer_id)
GROUP BY country
ORDER BY total_revenue DESC;


-- 22. Quantity Sold in Country

SELECT country, SUM(quantity) AS total_quantity
FROM sales_fact
JOIN customer_dimension USING(customer_id)
GROUP BY country
ORDER BY total_quantity DESC;


-- 23. Top Countries by Revenue

SELECT country, SUM(revenue) AS total_revenue
FROM sales_fact
JOIN customer_dimension USING(customer_id)
GROUP BY country
ORDER BY total_revenue DESC
LIMIT 10;


-- 24. Countries With Most Customers

SELECT country, COUNT(DISTINCT customer_id) AS customer_count
FROM customer_dimension
GROUP BY country
ORDER BY customer_count DESC;



-- -----------------------------------
-- f) Sales Behavior Analytics
-- -----------------------------------


-- 25. Average Order Value

SELECT AVG(revenue) AS avg_order_value
FROM sales_fact;


-- 26. Highest Single Transaction

SELECT MAX(revenue) AS highest_transaction
FROM sales_fact;


-- 27. Lowest Transaction Value

SELECT MIN(revenue) AS lowest_transaction
FROM sales_fact;


-- 28. Total Transactions per Customer

SELECT customer_id, COUNT(*) AS transactions
FROM sales_fact
GROUP BY customer_id
ORDER BY transactions DESC;



-- ------------------------------------
-- g) Warehouse Validation Queries
-- ------------------------------------


-- 29. Fact Table Size

SELECT COUNT(*) FROM sales_fact;


-- 30. Dimension Table Sizes

SELECT
    (SELECT COUNT(*) FROM product_dimension) AS products,
    (SELECT COUNT(*) FROM customer_dimension) AS customers,
    (SELECT COUNT(*) FROM date_dimension) AS dates;


-- =============================================================================================
