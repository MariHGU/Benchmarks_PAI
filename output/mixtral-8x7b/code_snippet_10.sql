SELECT oi.product_id, p.name, SUM(oi.quantity * oi.unit_price) as total_earned
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.name
ORDER BY total_earned DESC
LIMIT 1;