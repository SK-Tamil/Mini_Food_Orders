CREATE DATABASE IF NOT EXISTS fooddb;

USE fooddb;

CREATE TABLE IF NOT EXISTS foods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    image VARCHAR(255),
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    food_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status VARCHAR(30) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_order_food
        FOREIGN KEY (food_id)
        REFERENCES foods(id)
        ON DELETE CASCADE
);

INSERT INTO foods (name, category, price, image, available)
VALUES
('Chicken Burger', 'Burger', 120.00, 'chicken-burger.jpg', TRUE),
('Veg Pizza', 'Pizza', 180.00, 'veg-pizza.jpg', TRUE),
('French Fries', 'Snacks', 80.00, 'french-fries.jpg', TRUE),
('Cold Coffee', 'Drinks', 90.00, 'cold-coffee.jpg', TRUE);
