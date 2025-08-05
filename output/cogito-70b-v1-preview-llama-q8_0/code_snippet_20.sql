WITH TopSellingProducts AS (
    SELECT 
        p.product_id,
        p.name,
        SUM(oi.quantity) AS total_quantity
    FROM Products p
    JOIN OrderItems oi ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.name
    ORDER BY total_quantity DESC
    LIMIT 5
),
TopPaymentMethods AS (
    SELECT 
        tsp.product_id,
        pm.payment_method,
        COUNT(*) AS payment_count
    FROM TopSellingProducts tsp
    JOIN OrderItems oi ON tsp.product_id = oi.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments pm ON o.order_id = pm.order_id
    GROUP BY tsp.product_id, pm.payment_method
)
SELECT 
    product_name,
    payment_method,
    payment_count,
    RANK() OVER (PARTITION BY product_name ORDER BY payment_count DESC) AS rank
FROM (
    SELECT 
        p.name AS product_name,
        tp.payment_method,
        tp.payment_count
    FROM TopPaymentMethods tp
    JOIN Products p ON tp.product_id = p.product_id
) ranked_methods
WHERE rank = 1;