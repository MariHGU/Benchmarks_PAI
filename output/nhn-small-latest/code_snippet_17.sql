WITH Top5Products AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) AS total_sold
    FROM order_items oi
    GROUP BY oi.product_id
    ORDER BY total_sold DESC
    LIMIT 5
),
PaymentInfo AS (
    SELECT 
        p.payment_method,
        COUNT(*) AS payment_count
    FROM payments p
    JOIN orders o ON p.order_id = o.order_id
    WHERE EXISTS (
        SELECT 1 
        FROM order_items oi 
        WHERE oi.order_id = o.order_id 
        AND oi.product_id IN (SELECT product_id FROM Top5Products)
    )
    GROUP BY p.payment_method
)
SELECT payment_method, payment_count
FROM PaymentInfo
ORDER BY payment_count DESC;