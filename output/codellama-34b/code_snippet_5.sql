SELECT oi.*, p.price * oi.quantity AS total_revenue
FROM OrderItems oi
JOIN Orders o ON oi.order_id = o.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE o.total_amount > 0;