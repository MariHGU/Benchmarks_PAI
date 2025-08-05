SELECT 
    p.product_id, 
    SUM(oi.quantity) AS total_quantity
FROM 
    OrderItems oi
JOIN 
    Products p ON oi.product_id = p.product_id
GROUP BY 
    p.product_id
ORDER BY 
    total_quantity DESC
LIMIT 1;