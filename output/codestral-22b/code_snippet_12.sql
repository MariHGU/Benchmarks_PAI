SELECT p.name AS product_name, SUM(oi.quantity) AS total_sold, SUM(oi.unit_price * oi.quantity) AS total_earnings
FROM OrderItems AS oi
JOIN Products AS p ON oi.product_id = p.product_id
GROUP BY oi.product_id
ORDER BY total_sold DESC
LIMIT 1;