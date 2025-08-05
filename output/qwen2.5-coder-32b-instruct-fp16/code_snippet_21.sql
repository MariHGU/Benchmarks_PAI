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
CustomerOrderItems AS (
    SELECT 
        toi.customer_id,
        toi.product_id,
        SUM(toi.quantity) AS total_quantity_purchased
    FROM 
        TopCustomers tc
    JOIN 
        Orders o ON tc.customer_id = o.customer_id
    JOIN 
        OrderItems toi ON o.order_id = toi.order_id
    GROUP BY 
        toi.customer_id, toi.product_id
),
MostPurchasedItems AS (
    SELECT 
        coi.customer_id,
        coi.product_id,
        p.stock_qty,
        coi.total_quantity_purchased,
        ROW_NUMBER() OVER (PARTITION BY coi.customer_id ORDER BY coi.total_quantity_purchased DESC) as rn
    FROM 
        CustomerOrderItems coi
    JOIN 
        Products p ON coi.product_id = p.product_id
)
SELECT 
    mpi.customer_id,
    c.first_name,
    c.last_name,
    mpi.product_id,
    p.name AS product_name,
    p.stock_qty,
    mpi.total_quantity_purchased
FROM 
    MostPurchasedItems mpi
JOIN 
    Customers c ON mpi.customer_id = c.customer_id
JOIN 
    Products p ON mpi.product_id = p.product_id
WHERE 
    mpi.rn = 1
ORDER BY 
    p.stock_qty ASC;