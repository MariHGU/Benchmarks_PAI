WITH MostSoldItems AS (
    SELECT 
        product_id,
        SUM(quantity) as total_sold
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_sold DESC
    LIMIT 5
)
SELECT 
    p.name AS product_name,
    pm.payment_method,
    COUNT(*) as payment_count
FROM MostSoldItems msi
JOIN OrderItems oi ON msi.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments pm ON o.order_id = pm.order_id
GROUP BY p.name, pm.payment_method
ORDER BY payment_count DESC;