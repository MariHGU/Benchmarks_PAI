WITH Top5Products AS (
    SELECT 
        product_id,
        SUM(quantity) AS total_sold
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_sold DESC
    LIMIT 5
),
PaymentCounts AS (
    SELECT 
        t5p.product_id,
        pm.payment_method,
        COUNT(*) AS usage_count,
        ROW_NUMBER() OVER (PARTITION BY t5p.product_id ORDER BY COUNT(*) DESC) AS rn
    FROM Top5Products t5p
    JOIN OrderItems oi ON t5p.product_id = oi.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments pm ON o.order_id = pm.order_id
    GROUP BY t5p.product_id, pm.payment_method
)
SELECT 
    p.name AS product_name,
    pc.payment_method,
    pc.usage_count
FROM PaymentCounts pc
JOIN Products p ON pc.product_id = p.product_id
WHERE pc.rn = 1;