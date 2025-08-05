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
        o.item_id,
        p.payment_method
    FROM 
        TopSoldItems tsi
    JOIN 
        OrderItems o ON tsi.product_id = o.product_id
    JOIN 
        Payments p ON o.order_id = p.order_id
)
SELECT 
    item_id,
    payment_method,
    COUNT(*) AS usage_count
FROM 
    ItemPayments
GROUP BY 
    item_id, payment_method
ORDER BY 
    item_id, usage_count DESC;