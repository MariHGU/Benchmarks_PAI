-- Add new column
ALTER TABLE employees ADD COLUMN full_name VARCHAR(100);

-- Copy data
UPDATE employees SET full_name = emp_name;

-- Drop old column
ALTER TABLE employees DROP COLUMN emp_name;