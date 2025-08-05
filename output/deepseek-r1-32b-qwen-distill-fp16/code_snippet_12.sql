WITH TopProducts AS (
    SELECT 
        product_id,
        SUM(quantity) as total_sold
    FROM 
        OrderItems
    GROUP BY 
        product_id
    ORDER BY 
        total_sold DESC
    LIMIT 5
),
ProductPayments AS (
    SELECT 
        oi.product_id,
        p.payment_method,
        COUNT(*) as payment_count
    FROM 
        OrderItems oi
    JOIN 
        Orders o ON oi.order_id = o.order_id
    JOIN 
        Payments p ON o.order_id = p.order_id
    WHERE 
        oi.product_id IN (SELECT product_id FROM TopProducts)
    GROUP BY 
        oi.product_id, p.payment_method
)
SELECT 
    tp.product_id,
    pr.name AS product_name,
    pp.payment_method,
    pp.payment_count
FROM 
    TopProducts tp
JOIN 
    ProductPayments pp ON tp.product_id = pp.product_id
JOIN 
    Products pr ON tp.product_id = pr.product_id
ORDER BY 
    tp.product_id, pp.payment_count DESC;