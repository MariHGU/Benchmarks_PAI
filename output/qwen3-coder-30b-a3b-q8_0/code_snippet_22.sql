WITH top_5_items AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_sold
    FROM OrderItems oi
    GROUP BY oi.product_id
    ORDER BY total_quantity_sold DESC
    LIMIT 5
),
payment_counts AS (
    SELECT 
        t5i.product_id,
        p.payment_method,
        COUNT(*) AS payment_count
    FROM top_5_items t5i
    JOIN OrderItems oi ON t5i.product_id = oi.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments p ON o.order_id = p.order_id
    GROUP BY t5i.product_id, p.payment_method
)
SELECT 
    t5i.product_id,
    p.name AS product_name,
    pc.payment_method,
    pc.payment_count
FROM top_5_items t5i
JOIN Products p ON t5i.product_id = p.product_id
JOIN payment_counts pc ON t5i.product_id = pc.product_id
WHERE pc.payment_count = (
    SELECT MAX(payment_count) 
    FROM payment_counts pc2 
    WHERE pc2.product_id = t5i.product_id
)
ORDER BY t5i.total_quantity_sold DESC;