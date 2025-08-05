WITH CustomerOrderCount AS (
    SELECT 
        c.customer_id,
        COUNT(*) as order_count
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    ORDER BY order_count DESC
    LIMIT 5
)
SELECT DISTINCT
    p.name,
    SUM(oi.quantity) as total_quantity_purchased,
    p.stock_qty,
    p.category
FROM CustomerOrderCount coc
JOIN Orders o ON coc.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.name, p.stock_qty, p.category
ORDER BY p.stock_qty ASC;