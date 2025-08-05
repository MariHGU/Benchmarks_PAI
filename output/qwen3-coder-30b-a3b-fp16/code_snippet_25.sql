WITH top_5_customers AS (
    SELECT 
        customer_id,
        COUNT(*) AS total_orders
    FROM Orders
    GROUP BY customer_id
    ORDER BY total_orders DESC
    LIMIT 5
),
customer_item_counts AS (
    SELECT 
        t5c.customer_id,
        oi.product_id,
        SUM(oi.quantity) AS total_quantity_purchased
    FROM top_5_customers t5c
    JOIN Orders o ON t5c.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    GROUP BY t5c.customer_id, oi.product_id
),
top_items_per_customer AS (
    SELECT 
        customer_id,
        product_id,
        total_quantity_purchased,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY total_quantity_purchased DESC) as rn
    FROM customer_item_counts
)
SELECT 
    t5c.customer_id,
    c.first_name,
    c.last_name,
    p.product_id,
    p.name AS product_name,
    tipc.total_quantity_purchased,
    p.stock_qty
FROM top_5_customers t5c
JOIN Customers c ON t5c.customer_id = c.customer_id
JOIN top_items_per_customer tipc ON t5c.customer_id = tipc.customer_id
JOIN Products p ON tipc.product_id = p.product_id
WHERE tipc.rn = 1
ORDER BY p.stock_qty ASC;