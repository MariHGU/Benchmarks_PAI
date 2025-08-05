WITH TopSoldItems AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_sold
    FROM 
        OrderItems oi
    GROUP BY 
        oi.product_id
    ORDER BY 
        total_quantity_sold DESC
    LIMIT 5
),
ItemPayments AS (
    SELECT 
        o.product_id,
        p.payment_method
    FROM 
        TopSoldItems tsi
    JOIN 
        OrderItems o ON tsi.product_id = o.product_id
    JOIN 
        Payments p ON o.order_id = p.order_id
)
SELECT 
    ip.product_id,
    pm.name AS product_name,
    ip.payment_method,
    COUNT(*) AS usage_count
FROM 
    ItemPayments ip
JOIN 
    Products pm ON ip.product_id = pm.product_id
GROUP BY 
    ip.product_id, ip.payment_method, pm.name
ORDER BY 
    ip.product_id, usage_count DESC;