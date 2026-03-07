
CREATE DATABASE retail_dw;

USE retail_dw;



-- Product - Dimension Table 

CREATE TABLE product_dimension (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(20),
    product_name VARCHAR(255)
);



-- Customer - Dimension Table 

CREATE TABLE customer_dimension (
    customer_id INT PRIMARY KEY,
    country VARCHAR(100)
);



-- Date - Dimension Table

CREATE TABLE date_dimension (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    day INT,
    month INT,
    year INT
);



-- Central Fact - Table

CREATE TABLE sales_fact (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    date_id INT,
    quantity INT,
    revenue FLOAT,
    
    FOREIGN KEY (product_id) REFERENCES product_dimension(product_id),
    FOREIGN KEY (customer_id) REFERENCES customer_dimension(customer_id),
    FOREIGN KEY (date_id) REFERENCES date_dimension(date_id)
);




-- Check All Tables
SHOW TABLES;





-- SHOW / VIEW the data inserted into tables (10 rows per table)

SELECT * FROM product_dimension LIMIT 10;

SELECT * FROM customer_dimension LIMIT 10;

SELECT * FROM date_dimension LIMIT 10;

SELECT * FROM sales_fact LIMIT 10;




-- SHOW / VIEW the total no. of records in each table

SELECT COUNT(*) as Total_Records FROM product_dimension;

SELECT COUNT(*) as Total_Records FROM customer_dimension;

SELECT COUNT(*) as Total_Records FROM date_dimension;

SELECT COUNT(*) as Total_Records FROM sales_fact;




-- Add indexes to make fact table joins faster for dashboard

CREATE INDEX idx_product ON product_dimension(stock_code);
CREATE INDEX idx_customer ON customer_dimension(customer_id);
CREATE INDEX idx_date ON date_dimension(date);

