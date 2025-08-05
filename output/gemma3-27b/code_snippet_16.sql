WITH Top5Customers AS (
    SELECT
        customer_id
    FROM
        Orders
    GROUP BY
        customer_id
    ORDER BY
        COUNT(*) DESC
    LIMIT 5
),
CustomerItemCounts AS (
    SELECT
        o.customer_id,
        oi.product_id,
        p.name AS product_name,
        SUM(oi.quantity) AS total_quantity,
        p.stock_qty
    FROM
        Orders o
    JOIN
        OrderItems oi ON o.order_id = oi.order_id
    JOIN
        Products p ON oi.product_id = p.product_id
    WHERE o.customer_id IN (SELECT customer_id FROM Top5Customers)
    GROUP BY o.customer_id, oi.product_id, p.name, p.stock_qty
)
SELECT
    customer_id,
    product_id,
    product_name,
    total_quantity,
    stock_qty
FROM
    CustomerItemCounts
ORDER BY
    customer_id,
    stock_qty ASC;