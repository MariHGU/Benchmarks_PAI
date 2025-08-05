WITH TopCustomers AS (
    SELECT customer_id,
           COUNT(order_id) AS order_count
    FROM Orders
    GROUP BY customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
CustomerPurchaseItems AS (
    SELECT tc.customer_id,
           oi.product_id,
           p.name AS product_name,
           SUM(oi.quantity) AS total_quantity_purchased
    FROM TopCustomers tc
    JOIN Orders o ON tc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY tc.customer_id, oi.product_id, p.name
)
SELECT cpi.customer_id,
       cpi.product_name,
       SUM(cpi.total_quantity_purchased) AS total_quantity_purchased,
       p.stock_qty
FROM CustomerPurchaseItems cpi
JOIN Products p ON cpi.product_id = p.product_id
GROUP BY cpi.customer_id, cpi.product_name, p.stock_qty
ORDER BY p.stock_qty ASC;