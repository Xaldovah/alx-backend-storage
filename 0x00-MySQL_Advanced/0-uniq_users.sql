-- Create a table named 'users' if it does not already exist
-- The table includes an auto-incremented 'id', a unique 'email' field, and a 'name' field
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
