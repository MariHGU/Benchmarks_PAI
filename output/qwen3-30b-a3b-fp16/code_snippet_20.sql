WITH top_products AS (
    SELECT 
        p.product_id,
        p.name,
        SUM(oi.quantity) AS total_quantity
    FROM OrderItems oi
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.name
    ORDER BY total_quantity DESC
    LIMIT 5
),
product_payments AS (
    SELECT 
        tp.product_id,
        tp.name AS product_name,
        p.payment_method,
        COUNT(*) AS payment_count,
        ROW_NUMBER() OVER (PARTITION BY tp.product_id ORDER BY COUNT(*) DESC) AS rn
    FROM top_products tp
    JOIN OrderItems oi ON tp.product_id = oi.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments p ON o.order_id = p.order_id
    GROUP BY tp.product_id, tp.name, p.payment_method
)
SELECT 
    product_id,
    product_name,
    payment_method,
    payment_count
FROM product_payments
WHERE rn = 1;