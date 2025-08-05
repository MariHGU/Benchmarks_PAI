WITH Top5Items AS (
    SELECT
        product_id
    FROM
        OrderItems
    GROUP BY
        product_id
    ORDER BY
        SUM(quantity) DESC
    LIMIT 5
),
PaymentCounts AS (
    SELECT
        oi.product_id,
        p.payment_method,
        COUNT(*) AS payment_count,
        ROW_NUMBER() OVER (PARTITION BY oi.product_id ORDER BY COUNT(*) DESC) AS rn
    FROM
        OrderItems oi
    JOIN
        Orders o ON oi.order_id = o.order_id
    JOIN
        Payments p ON o.order_id = p.order_id
    WHERE oi.product_id IN (SELECT product_id FROM Top5Items)
    GROUP BY oi.product_id, p.payment_method
)
SELECT
    product_id,
    payment_method,
    payment_count
FROM
    PaymentCounts
WHERE rn = 1;