WITH TopCustomers AS (
    SELECT c.customer_id,
           COUNT(o.order_id) AS order_count
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
TopItemsForTopCustomers AS (
    SELECT tc.customer_id,
           oi.product_id,
           SUM(oi.quantity) AS total_quantity_purchased
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    GROUP BY tc.customer_id, oi.product_id
)
SELECT ti.product_id,
       p.name AS product_name,
       SUM(ti.total_quantity_purchased) AS total_quantity_purchased,
       p.stock_qty
FROM TopItemsForTopCustomers ti
JOIN Products p ON ti.product_id = p.product_id
GROUP BY ti.product_id, p.name, p.stock_qty
ORDER BY p.stock_qty ASC;