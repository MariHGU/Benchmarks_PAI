-- Original: VARCHAR(50) NOT NULL
ALTER TABLE users CHANGE COLUMN email_address user_email VARCHAR(50) NOT NULL;

-- Original: INT(11) DEFAULT 0
ALTER TABLE products CHANGE COLUMN price cost_price INT(11) DEFAULT 0;