WITH CustomerOrders AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count
    FROM Orders
    GROUP BY customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
TopItemsByCustomer AS (
    SELECT 
        c.customer_id,
        p.name AS product_name,
        SUM(oi.quantity) as total_quantity
    FROM CustomerOrders co
    JOIN Customers c ON co.customer_id = c.customer_id
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY c.customer_id, p.name
)
SELECT 
    ti.customer_id,
    ti.product_name,
    p.stock_qty as stock,
    ti.total_quantity
FROM TopItemsByCustomer ti
JOIN Products p ON ti.product_name = p.name
ORDER BY ti.customer_id, p.stock_qty ASC;