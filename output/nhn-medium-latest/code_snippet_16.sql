WITH TopSoldItems AS (
    SELECT product_id,
           SUM(quantity) AS total_quantity_sold
    FROM OrderItems
    GROUP BY product_id
    ORDER BY total_quantity_sold DESC
    LIMIT 5
),
PaymentMethods AS (
    SELECT pmi.product_id,
           pm.payment_method,
           COUNT(pm.order_id) AS payment_count
    FROM TopSoldItems pmi
    JOIN OrderItems oi ON pmi.product_id = oi.product_id
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments pm ON o.order_id = pm.order_id
    GROUP BY pmi.product_id, pm.payment_method
)
SELECT product_id,
       payment_method,
       payment_count
FROM PaymentMethods
ORDER BY product_id ASC, payment_count DESC;