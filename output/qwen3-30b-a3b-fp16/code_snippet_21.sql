WITH top_customers AS (
    SELECT 
        customer_id
    FROM Orders
    GROUP BY customer_id
    ORDER BY COUNT(*) DESC
    LIMIT 5
),
customer_products AS (
    SELECT 
        tc.customer_id,
        p.product_id,
        p.name,
        SUM(oi.quantity) AS total_quantity,
        ROW_NUMBER() OVER (PARTITION BY tc.customer_id ORDER BY SUM(oi.quantity) DESC) AS rn
    FROM top_customers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY tc.customer_id, p.product_id, p.name
)
SELECT 
    cp.customer_id,
    cp.product_id,
    cp.name,
    p.stock_qty
FROM customer_products cp
JOIN Products p ON cp.product_id = p.product_id
WHERE cp.rn = 1
ORDER BY p.stock_qty ASC;