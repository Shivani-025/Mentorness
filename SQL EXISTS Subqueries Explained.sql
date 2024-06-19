
USE MyNewDatabase;

-- Create a table
CREATE TABLE IF NOT EXISTS MyNewTable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);

SELECT customer_id, customer_name
FROM employees e
WHERE EXISTS (
    SELECT 1
    FROM salaries s 
    WHERE s.employee_id = e.id
    AND s.amount > 50000
);
