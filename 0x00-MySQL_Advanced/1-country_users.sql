-- SQL script to create a 'users' table with specific attributes
-- The table includes the following columns:
-- id: An integer that serves as the primary key, auto-incremented, and cannot be null.
-- email: A string (maximum 255 characters) that must be unique and cannot be null.
-- name: A string (maximum 255 characters) that represents the user's name (optional).
-- country: An enumeration of countries (US, CO, TN) that cannot be null, with a default value of 'US'.

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);

