WITH TopProducts AS (
    SELECT 
        product_id,
        SUM(quantity) AS total_sold
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_sold DESC
    LIMIT 5
),
OrderWithTopProducts AS (
    SELECT DISTINCT order_id
    FROM OrderItems
    WHERE product_id IN (SELECT product_id FROM TopProducts)
),
PaymentMethodCount AS (
    SELECT 
        payment_method,
        COUNT(*) AS count
    FROM Payments p
    JOIN OrderWithTopProducts owp ON p.order_id = owp.order_id
    GROUP BY payment_method
)
SELECT 
    payment_method,
    count
FROM PaymentMethodCount
ORDER BY count DESC;