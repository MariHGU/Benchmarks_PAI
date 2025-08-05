WITH TopSoldItems AS (
    SELECT 
        product_id,
        SUM(quantity) as total_sold
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_sold DESC
    LIMIT 5
)
SELECT 
    tsi.product_id,
    p.name AS product_name,
    pm.payment_method,
    COUNT(p.payment_method) as payment_count
FROM TopSoldItems tsi
JOIN OrderItems oi ON tsi.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments p ON o.order_id = p.order_id
GROUP BY tsi.product_id, p.name, pm.payment_method
ORDER BY tsi.product_id, payment_count DESC;