SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    p.product_id,
    pr.name AS product_name,
    SUM(oi.quantity) AS total_quantity_purchased
FROM 
    Customers c
JOIN 
    Orders o ON c.customer_id = o.customer_id
JOIN 
    OrderItems oi ON o.order_id = oi.order_id
JOIN 
    Products pr ON oi.product_id = pr.product_id
GROUP BY 
    c.customer_id, c.first_name, c.last_name, p.product_id, pr.name
HAVING COUNT(o.order_id) > (
        SELECT 
            COUNT(o2.order_id)
        FROM 
            Orders o2
        GROUP BY 
            o2.customer_id
        ORDER BY 
            COUNT(*) DESC
        LIMIT 1 OFFSET 5
    )
ORDER BY 
    total_quantity_purchased ASC, pr.stock_qty ASC;