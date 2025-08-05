WITH TopSoldItems AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_sold
    FROM
        OrderItems oi
    GROUP BY
        oi.product_id
    ORDER BY
        total_quantity_sold DESC
    LIMIT 5
),
TopPaymentMethods AS (
    SELECT
        pmi.order_id,
        pmi.payment_method,
        ROW_NUMBER() OVER (PARTITION BY pmi.order_id ORDER BY pmi.amount DESC) as rn
    FROM
        Payments pmi
)
SELECT
    tsi.product_id,
    pm.payment_method,
    COUNT(*) AS payment_count
FROM
    TopSoldItems tsi
JOIN
    Orders o ON tsi.product_id IN (SELECT product_id FROM OrderItems WHERE order_id = o.order_id)
JOIN
    Payments pm ON o.order_id = pm.order_id
GROUP BY
    tsi.product_id, pm.payment_method
ORDER BY
    payment_count DESC;