SELECT 
    p2.payment_method, 
    COUNT(*) AS count
FROM 
    OrderItems oi
JOIN 
    Orders o ON oi.order_id = o.order_id
JOIN 
    Payments p2 ON o.order_id = p2.order_id
WHERE 
    oi.product_id IN (
        SELECT 
            product_id 
        FROM 
            OrderItems
        GROUP BY 
            product_id
        ORDER BY 
            SUM(quantity) DESC
        LIMIT 5
    )
GROUP BY 
    p2.payment_method
ORDER BY 
    count DESC
LIMIT 1;