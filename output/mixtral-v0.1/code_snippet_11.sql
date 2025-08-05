WITH MostSoldItems AS (
    SELECT oi.product_id, p.name as product_name, SUM(oi.quantity) as total_sold_qty
    FROM OrderItems oi
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY oi.product_id
    ORDER BY total_sold_qty DESC
    LIMIT 5
)
SELECT msi.product_name, pm.payment_method as most_used_payment_method, COUNT(*) AS payment_count
FROM MostSoldItems msi
JOIN OrderItems oi ON msi.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN Payments pmt ON o.order_id = pmt.order_id
JOIN PaymentMethods pm ON pmt.payment_method = pm.name
GROUP BY msi.product_name, pm.payment_method
ORDER BY payment_count DESC;