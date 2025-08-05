WITH top_5_products AS (
    SELECT 
        oi.product_id,
        p.name AS product_name,
        ROW_NUMBER() OVER (ORDER BY SUM(oi.quantity) DESC) AS row_num
    FROM OrderItems oi
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY oi.product_id, p.name
)
SELECT 
    pm.payment_method,
    COUNT(pm.payment_method) AS payment_count
FROM Payments pm
JOIN Orders o ON pm.order_id = o.order_id
JOIN OrderItems oi ON o.order_id = oi.order_id
WHERE oi.product_id IN (
    SELECT product_id FROM top_5_products WHERE row_num <= 5
)
GROUP BY pm.payment_method
ORDER BY payment_count DESC
LIMIT 1;