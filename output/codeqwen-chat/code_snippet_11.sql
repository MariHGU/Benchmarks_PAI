SELECT o.product_id, p.name AS product_name, SUM(oi.quantity) AS total_sold, SUM(oi.unit_price * oi.quantity) AS earnings
FROM Orders o
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY o.product_id, p.name
ORDER BY total_sold DESC
LIMIT 1;