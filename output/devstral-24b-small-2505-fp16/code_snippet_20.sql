SELECT p.name AS product_name,
       SUM(oi.quantity) AS total_quantity_sold
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.name
ORDER BY total_quantity_sold DESC
LIMIT 5;