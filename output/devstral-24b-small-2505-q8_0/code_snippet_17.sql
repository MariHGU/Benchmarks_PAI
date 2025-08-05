WITH TopSoldItems AS (
    SELECT oi.product_id,
           SUM(oi.quantity) AS total_quantity_sold
    FROM OrderItems oi
    GROUP BY oi.product_id
    ORDER BY total_quantity_sold DESC
    LIMIT 5
),
OrderPayments AS (
    SELECT o.order_id, p.payment_method
    FROM Orders o
    JOIN Payments p ON o.order_id = p.order_id
)
SELECT tsi.product_id,
       p.name AS product_name,
       op.payment_method,
       COUNT(op.order_id) AS payment_count
FROM TopSoldItems tsi
JOIN OrderItems oi ON tsi.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN OrderPayments op ON o.order_id = op.order_id
JOIN Products p ON tsi.product_id = p.product_id
GROUP BY tsi.product_id, p.name, op.payment_method
ORDER BY payment_count DESC;