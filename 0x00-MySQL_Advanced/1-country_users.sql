-- The table includes an auto-incremented 'id', a unique 'email' field,
-- a 'name' field, and a 'country' field with an enumeration constraint
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
