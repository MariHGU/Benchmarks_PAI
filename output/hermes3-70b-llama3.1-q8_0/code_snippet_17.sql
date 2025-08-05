SELECT oi.product_id, p.name, SUM(oi.quantity) AS total_quantity_sold, 
       SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.name
ORDER BY total_quantity_sold DESC
LIMIT 1;