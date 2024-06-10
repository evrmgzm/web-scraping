CREATE TABLE IF NOT EXISTS petlebi (
    product_id INT PRIMARY KEY,
    product_url VARCHAR(255),
    product_name VARCHAR(255),
    product_barcode VARCHAR(255),
    product_price VARCHAR(20),
    product_stock VARCHAR(10),
    description TEXT,
    brand VARCHAR(100),
    category VARCHAR(255),
    sku VARCHAR(255)
);
