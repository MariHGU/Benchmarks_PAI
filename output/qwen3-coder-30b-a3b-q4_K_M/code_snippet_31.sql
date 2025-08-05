WITH Top5Customers AS (
    SELECT 
        o.customer_id,
        COUNT(*) as total_orders
    FROM Orders o
    GROUP BY o.customer_id
    ORDER BY total_orders DESC
    LIMIT 5
),
CustomerItemPurchases AS (
    SELECT 
        t5c.customer_id,
        oi.product_id,
        SUM(oi.quantity) as total_quantity_purchased
    FROM Top5Customers t5c
    JOIN Orders o ON t5c.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    GROUP BY t5c.customer_id, oi.product_id
),
TopItemsByCustomer AS (
    SELECT 
        cip.customer_id,
        cip.product_id,
        cip.total_quantity_purchased,
        ROW_NUMBER() OVER (PARTITION BY cip.customer_id ORDER BY cip.total_quantity_purchased DESC) as rn
    FROM CustomerItemPurchases cip
)
SELECT 
    p.name AS product_name,
    p.stock_qty,
    t.customer_id,
    t.total_quantity_purchased
FROM TopItemsByCustomer t
JOIN Products p ON t.product_id = p.product_id
WHERE t.rn = 1
ORDER BY p.stock_qty ASC;