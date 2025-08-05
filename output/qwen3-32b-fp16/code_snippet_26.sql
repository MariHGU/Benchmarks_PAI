WITH TopCustomers AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_orders
    FROM Orders
    GROUP BY customer_id
    ORDER BY total_orders DESC
    LIMIT 5
),
CustomerProducts AS (
    SELECT 
        tc.customer_id,
        oi.product_id,
        SUM(oi.quantity) AS total_purchased
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    GROUP BY tc.customer_id, oi.product_id
),
RankedProducts AS (
    SELECT 
        customer_id,
        product_id,
        total_purchased,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY total_purchased DESC) AS rn
    FROM CustomerProducts
)
SELECT 
    p.name AS product_name,
    p.stock_qty
FROM RankedProducts rp
JOIN Products p ON rp.product_id = p.product_id
WHERE rp.rn = 1
ORDER BY p.stock_qty ASC;