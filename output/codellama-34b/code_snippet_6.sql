SELECT oi.*, p.payment_method
FROM OrderItems oi
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments p ON o.payment_id = p.payment_id
WHERE o.total_amount > 0;