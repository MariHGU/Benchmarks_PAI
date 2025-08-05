WITH top_5_customers AS (
    SELECT 
        c.customer_id,
        c.first_name,
        c.last_name,
        ROW_NUMBER() OVER (ORDER BY COUNT(o.order_id) DESC) AS row_num
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.first_name, c.last_name
)
SELECT 
    t5.first_name AS customer_first_name,
    t5.last_name AS customer_last_name,
    p.name AS product_name,
    SUM(oi.quantity) AS quantity_purchased,
    p.stock_qty AS stock_quantity
FROM top_5_customers t5
JOIN Orders o ON t5.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE t5.row_num <= 5
GROUP BY t5.first_name, t5.last_name, p.name, p.stock_qty
ORDER BY stock_quantity ASC;