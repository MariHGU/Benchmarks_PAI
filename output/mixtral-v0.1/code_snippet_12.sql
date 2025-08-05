WITH MostOrderingCustomers AS (
    SELECT o.customer_id, c.first_name || ' ' || c.last_name as customer_name, COUNT(o.order_id) as order_count
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    GROUP BY o.customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
MostFrequentItems AS (
    SELECT moc.customer_name, oi.product_id, p.name as product_name, SUM(oi.quantity) as total_purchased_qty, p.stock_qty
    FROM MostOrderingCustomers moc
    JOIN Orders o ON moc.customer_id = o.customer_id
    JOIN OrderItems oi ON o.order_id = oi.order_id
    JOIN Products p on oi.product_id = p.product_id
    GROUP BY moc.customer_name, oi.product_id
    ORDER BY total_purchased_qty DESC
)
SELECT customer_name, product_name, stock_qty, total_purchased_qty FROM MostFrequentItems
ORDER BY stock_qty ASC;