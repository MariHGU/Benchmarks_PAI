SELECT oi.*, c.customer_id
FROM OrderItems oi
JOIN Orders o ON oi.order_id = o.order_id
JOIN Customers c ON o.customer_id = c.customer_id
WHERE o.total_amount > 0;