WITH TopCustomers AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        COUNT(o.order_id) AS order_count
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    ORDER BY order_count DESC
    LIMIT 5
),
CustomerItemPreferences AS (
    SELECT 
        tc.customer_id,
        tc.first_name,
        tc.last_name,
        p.product_id,
        p.name AS product_name,
        p.stock_qty,
        SUM(oi.quantity) AS total_quantity_purchased
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY tc.customer_id, tc.first_name, tc.last_name, p.product_id, p.name, p.stock_qty
)
SELECT 
    first_name,
    last_name,
    product_name,
    total_quantity_purchased,
    stock_qty
FROM CustomerItemPreferences
ORDER BY first_name, last_name, total_quantity_purchased DESC, stock_qty ASC;