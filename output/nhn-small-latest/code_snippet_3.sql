ALTER TABLE employees ADD COLUMN salary DECIMAL(10,2);
UPDATE employees SET salary = old_salary;
ALTER TABLE employees DROP COLUMN old_salary;