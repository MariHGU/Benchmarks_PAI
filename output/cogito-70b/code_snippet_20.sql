WITH Top5Sold AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) as quantity_sold
    FROM OrderItems oi
    GROUP BY oi.product_id
    ORDER BY quantity_sold DESC
    LIMIT 5
)
SELECT 
    pm.payment_method,
    COUNT(*) as payment_count
FROM Payments pm
JOIN Orders o ON pm.order_id = o.order_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Top5Sold t5s ON oi.product_id = t5s.product_id
GROUP BY pm.payment_method
ORDER BY payment_count DESC;