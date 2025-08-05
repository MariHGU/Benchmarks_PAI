WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) as total_orders
    FROM Orders
    GROUP BY customer_id
    ORDER BY total_orders DESC
    LIMIT 5
)
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    p.product_id,
    p.name AS product_name,
    SUM(oi.quantity) as total_quantity_purchased,
    p.stock_qty
FROM TopCustomers tc
JOIN Orders o ON tc.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
JOIN Customers c ON tc.customer_id = c.customer_id
GROUP BY 
    c.customer_id,
    c.first_name,
    c.last_name,
    p.product_id,
    p.name,
    p.stock_qty
ORDER BY 
    customer_id,
    total_quantity_purchased DESC,
    stock_qty ASC;