SELECT pm.payment_method, COUNT(*) AS payment_count
FROM Payments pm
JOIN Orders o ON pm.order_id = o.order_id
JOIN OrderItems oi ON o.order_id = oi.order_id
WHERE oi.product_id IN (
    SELECT product_id
    FROM OrderItems
    GROUP BY product_id
    ORDER BY SUM(quantity) DESC
    LIMIT 5
)
GROUP BY pm.payment_method
ORDER BY payment_count DESC
LIMIT 1;