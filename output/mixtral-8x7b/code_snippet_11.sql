SELECT pm.payment_method, COUNT(*) as num_orders
FROM Payments p
JOIN Orders o ON p.order_id = o.order_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE p.payment_date BETWEEN 'start date' AND 'end date'
GROUP BY pm.payment_method
ORDER BY num_orders DESC
LIMIT 5;