SELECT 
    pm.payment_method,
    SUM(oi.quantity) AS total_quantity_sold
FROM 
    OrderItems oi
JOIN 
    Orders o ON oi.order_id = o.order_id
JOIN 
    Payments p ON o.order_id = p.order_id
JOIN 
    Products pr ON oi.product_id = pr.product_id
JOIN 
    (SELECT 
        product_id,
        COUNT(*) AS item_count
     FROM 
        OrderItems
     GROUP BY 
        product_id
     ORDER BY 
        item_count DESC
     LIMIT 5) top_sold_items ON oi.product_id = top_sold_items.product_id
JOIN 
    PaymentMethods pm ON p.payment_method = pm.payment_method
GROUP BY 
    pm.payment_method
ORDER BY 
    total_quantity_sold DESC
LIMIT 1;