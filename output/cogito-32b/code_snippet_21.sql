WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(order_id) as order_count
    FROM Orders
    GROUP BY customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
CustomerOrders AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        oi.product_id,
        p.name AS product_name,
        p.stock_qty as stock_quantity,
        SUM(oi.quantity) as total_purchased
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    JOIN Customers c ON o.customer_id = c.customer_id
    GROUP BY 
        c.customer_id,
        c.first_name,
        c.last_name,
        oi.product_id,
        p.name,
        p.stock_qty
)
SELECT *
FROM CustomerOrders
ORDER BY customer_id, stock_quantity ASC;