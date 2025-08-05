WITH TopCustomers AS (
    SELECT
        c.customer_id,
        COUNT(o.order_id) AS order_count
    FROM
        Customers c
    JOIN
        Orders o ON c.customer_id = o.customer_id
    GROUP BY
        c.customer_id
    ORDER BY
        order_count DESC
    LIMIT 5
),
TopPurchasedItems AS (
    SELECT
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_purchased
    FROM
        OrderItems oi
    JOIN
        Orders o ON oi.order_id = o.order_id
    WHERE
        o.customer_id IN (SELECT customer_id FROM TopCustomers)
    GROUP BY
        oi.product_id
    ORDER BY
        total_quantity_purchased DESC
),
ItemStock AS (
    SELECT
        p.product_id,
        p.stock_qty
    FROM
        Products p
)
SELECT
    i.product_id,
    p.name AS product_name,
    i.total_quantity_purchased,
    s.stock_qty
FROM
    TopPurchasedItems i
JOIN
    ItemStock s ON i.product_id = s.product_id
ORDER BY
    s.stock_qty ASC;