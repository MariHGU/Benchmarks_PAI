WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(order_id) AS order_count
    FROM 
        Orders
    GROUP BY 
        customer_id
    ORDER BY 
        order_count DESC
    LIMIT 5
),
CustomerItems AS (
    SELECT 
        t.customer_id,
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_ordered
    FROM 
        TopCustomers t
    JOIN 
        Orders o ON t.customer_id = o.customer_id
    JOIN 
        OrderItems oi ON o.order_id = oi.order_id
    GROUP BY 
        t.customer_id, oi.product_id
),
MostOrderedItemsPerCustomer AS (
    SELECT 
        ci.customer_id,
        ci.product_id,
        p.name AS product_name,
        ci.total_quantity_ordered,
        RANK() OVER (PARTITION BY ci.customer_id ORDER BY ci.total_quantity_ordered DESC) as rank_order
    FROM 
        CustomerItems ci
    JOIN 
        Products p ON ci.product_id = p.product_id
)
SELECT 
    moi.customer_id,
    moi.product_id,
    moi.product_name,
    moi.total_quantity_ordered,
    pr.stock_qty
FROM 
    MostOrderedItemsPerCustomer moi
JOIN 
    Products pr ON moi.product_id = pr.product_id
WHERE 
    moi.rank_order = 1
ORDER BY 
    pr.stock_qty ASC;