SELECT 
    p.payment_method,
    COUNT(*) AS num_times_used
FROM 
    Payments p
JOIN 
    Orders o ON p.order_id = o.order_id
JOIN 
    OrderItems oi ON o.order_id = oi.order_id
JOIN 
    Products pr ON oi.product_id = pr.product_id
GROUP BY 
    p.payment_method
ORDER BY 
    num_times_used DESC
LIMIT 5;