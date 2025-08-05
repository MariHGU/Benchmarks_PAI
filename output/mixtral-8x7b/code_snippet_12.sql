SELECT c.customer_id, p.product_id, p.name, SUM(oi.quantity) as total_quantity, p.stock_qty
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY c.customer_id, p.product_id, p.name, p.stock_qty
ORDER BY total_quantity DESC, p.stock_qty ASC
LIMIT 5;