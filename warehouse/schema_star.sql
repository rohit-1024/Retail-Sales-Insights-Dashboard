
-- CREATE DATABASE retail_dw;

-- USE retail_dw;



-- Product - Dimension Table 

-- CREATE TABLE product_dimension (
--     product_id INT AUTO_INCREMENT PRIMARY KEY,
--     stock_code VARCHAR(20),
--     product_name VARCHAR(255)
-- );



-- Customer - Dimension Table 

-- CREATE TABLE customer_dimension (
--     customer_id INT PRIMARY KEY,
--     country VARCHAR(100)
-- );



-- Date - Dimension Table

-- CREATE TABLE date_dimension (
--     date_id INT AUTO_INCREMENT PRIMARY KEY,
--     date DATE,
--     day INT,
--     month INT,
--     year INT
-- );



-- Central Fact - Table

-- CREATE TABLE sales_fact (
--     sale_id INT AUTO_INCREMENT PRIMARY KEY,
--     product_id INT,
--     customer_id INT,
--     date_id INT,
--     quantity INT,
--     revenue FLOAT,
--     
--     FOREIGN KEY (product_id) REFERENCES product_dimension(product_id),
--     FOREIGN KEY (customer_id) REFERENCES customer_dimension(customer_id),
--     FOREIGN KEY (date_id) REFERENCES date_dimension(date_id)
-- );



-- Check All Tables
-- SHOW TABLES;


