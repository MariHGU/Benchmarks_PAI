WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(order_id) as total_orders
    FROM 
        Orders
    GROUP BY 
        customer_id
    ORDER BY 
        total_orders DESC
    LIMIT 5
),
CustomerPurchases AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) as total_purchased
    FROM 
        OrderItems oi
    JOIN 
        TopCustomers tc ON oi.customer_id = tc.customer_id
    GROUP BY 
        oi.product_id
    ORDER BY 
        total_purchased DESC
)
SELECT 
    cp.product_id,
    p.name AS product_name,
    p.stock_qty,
    cp.total_purchased
FROM 
    CustomerPurchases cp
JOIN 
    Products p ON cp.product_id = p.product_id
ORDER BY 
    p.stock_qty ASC;