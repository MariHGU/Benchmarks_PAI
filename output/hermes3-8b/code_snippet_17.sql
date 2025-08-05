SELECT 
    pr.name AS product_name,
    SUM(oi.quantity) AS total_purchases,
    p.stock_qty AS current_stock
FROM 
    OrderItems oi
JOIN 
    Orders o ON oi.order_id = o.order_id
JOIN 
    Customers c ON o.customer_id = c.customer_id
JOIN 
    Products pr ON oi.product_id = pr.product_id
JOIN 
    (SELECT 
        customer_id,
        COUNT(*) AS order_count
     FROM 
        Orders
     GROUP BY 
        customer_id
     ORDER BY 
        order_count DESC
     LIMIT 5) top_order_customers ON c.customer_id = top_order_customers.customer_id
GROUP BY 
    pr.name, p.stock_qty
ORDER BY 
    total_purchases DESC;