WITH Top5Items AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) AS total_quantity
    FROM OrderItems oi
    GROUP BY oi.product_id
    ORDER BY total_quantity DESC
    LIMIT 5
),
PaymentMethodStats AS (
    SELECT 
        t5i.product_id,
        p.payment_method,
        COUNT(*) as payment_count,
        SUM(p.amount) as total_amount
    FROM Top5Items t5i
    JOIN Orders o ON o.order_id IN (
        SELECT oi.order_id 
        FROM OrderItems oi 
        WHERE oi.product_id = t5i.product_id
    )
    JOIN Payments p ON o.order_id = p.order_id
    GROUP BY t5i.product_id, p.payment_method
)
SELECT 
    p.name AS product_name,
    pm.payment_method,
    pm.payment_count
FROM PaymentMethodStats pm
JOIN Products p ON pm.product_id = p.product_id
WHERE pm.payment_count = (
    SELECT MAX(payment_count) 
    FROM PaymentMethodStats pm2 
    WHERE pm2.product_id = pm.product_id
)
ORDER BY p.name;