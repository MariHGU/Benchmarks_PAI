SELECT 
    p.product_id, 
    p.name, 
    SUM(oi.quantity) AS total_quantity, 
    p.stock_qty
FROM 
    Customers c
JOIN 
    Orders o ON c.customer_id = o.customer_id
JOIN 
    OrderItems oi ON o.order_id = oi.order_id
JOIN 
    Products p ON oi.product_id = p.product_id
WHERE 
    c.customer_id IN (
        SELECT 
            customer_id 
        FROM 
            Orders 
        GROUP BY 
            customer_id 
        ORDER BY 
            COUNT(*) DESC 
        LIMIT 5
    )
GROUP BY 
    p.product_id, 
    p.name, 
    p.stock_qty
ORDER BY 
    total_quantity DESC, 
    p.stock_qty ASC
LIMIT 5;