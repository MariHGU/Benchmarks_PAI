SELECT oi.product_id, p.name AS product_name, SUM(oi.quantity) as total_sold_qty, SUM((oi.unit_price * oi.quantity)) AS revenue
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY oi.product_id
ORDER BY total_sold_qty DESC, revenue DESC
LIMIT 1;