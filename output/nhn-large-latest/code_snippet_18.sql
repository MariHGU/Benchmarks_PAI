WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS total_orders
    FROM Orders
    GROUP BY customer_id
    ORDER BY total_orders DESC
    LIMIT 5
),
CustomerOrderItems AS (
    SELECT 
        oi.customer_id,
        oi.product_id,
        SUM(oi.quantity) AS total_purchased
    FROM OrderItems oi
    WHERE oi.customer_id IN (SELECT customer_id FROM TopCustomers)
    GROUP BY oi.customer_id, oi.product_id
),
MostPurchasedByCustomer AS (
    SELECT 
        customer_id,
        product_id,
        total_purchased,
        RANK() OVER(PARTITION BY customer_id ORDER BY total_purchased DESC) AS rank
    FROM CustomerOrderItems
)
SELECT 
    mcpc.customer_id,
    p.product_id,
    p.name AS product_name,
    p.stock_qty,
    mcpc.total_purchased
FROM MostPurchasedByCustomer mcpc
JOIN Products p ON mcpc.product_id = p.product_id
WHERE mcpc.rank = 1
ORDER BY p.stock_qty ASC;