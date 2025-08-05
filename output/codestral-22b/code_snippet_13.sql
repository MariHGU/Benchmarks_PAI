SELECT p.payment_method, COUNT(p.payment_id) AS usage_count
FROM Payments AS p
JOIN Orders AS o ON p.order_id = o.order_id
JOIN OrderItems AS oi ON o.order_id = oi.order_id
WHERE oi.product_id IN (
    SELECT product_id
    FROM OrderItems
    GROUP BY product_id
    ORDER BY SUM(quantity) DESC
    LIMIT 5
)
GROUP BY p.payment_method
ORDER BY usage_count DESC;