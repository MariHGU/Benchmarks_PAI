WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(*) as order_count
    FROM Orders
    GROUP BY customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
CustomerPurchaseHistory AS (
    SELECT 
        tc.customer_id,
        oi.product_id,
        p.name AS product_name,
        SUM(oi.quantity) as total_purchased,
        p.stock_qty
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY tc.customer_id, oi.product_id, p.name, p.stock_qty
)
SELECT 
    c.first_name,
    c.last_name,
    cph.product_name,
    cph.total_purchased,
    cph.stock_qty
FROM CustomerPurchaseHistory cph
JOIN Customers c ON cph.customer_id = c.customer_id
ORDER BY cph.stock_qty ASC;