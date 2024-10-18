-- SQL script that creates a table users following these requirements:
-- with the attribute:
-- id, email, name

CREATE TABLE IF NOT EXISTS users (
	id SERIAL PRIMARY KEY,
	email VARCHAR(225) NOT NULL UNIQUE,
	name VARCHAR(225) 
	);
