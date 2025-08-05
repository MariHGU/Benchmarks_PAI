WITH TopSellingProducts AS (
    SELECT 
        product_id,
        SUM(quantity) as total_quantity
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_quantity DESC
    LIMIT 5
)
SELECT 
    p.name AS product_name,
    pm.payment_method,
    COUNT(*) AS payment_count,
    SUM(p.amount) AS total_payments
FROM TopSellingProducts tsp
JOIN OrderItems oi ON tsp.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY product_name, pm.payment_method
ORDER BY payment_count DESC;