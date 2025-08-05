WITH Top5Customers AS (
    SELECT 
        c.customer_id,
        COUNT(o.order_id) AS total_orders
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
    ORDER BY total_orders DESC
    LIMIT 5
),
CustomerPurchases AS (
    SELECT 
        c.customer_id,
        p.product_id,
        SUM(oi.quantity) AS items_purchased,
        p.stock_qty
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE c.customer_id IN (SELECT customer_id FROM Top5Customers)
    GROUP BY c.customer_id, p.product_id, p.stock_qty
    ORDER BY items_purchased DESC, stock_qty ASC
)
SELECT 
    first_name,
    last_name,
    product_id,
    items_purchased,
    stock_qty
FROM CustomerPurchases cp
JOIN customers c ON cp.customer_id = c.customer_id
ORDER BY items_purchased DESC, stock_qty;