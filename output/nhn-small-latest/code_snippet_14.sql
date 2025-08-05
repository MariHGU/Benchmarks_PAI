WITH TopProducts AS (
    SELECT 
        p.name,
        COUNT(oi.order_item_id) AS units_sold
    FROM OrderItems oi
    JOIN Products p ON oi.product_id = p.product_id
    GROUP BY p.name, oi.unit_price
    ORDER BY units_sold DESC
    LIMIT 5
),
PaymentStats AS (
    SELECT 
        tp.name,
        pym.payment_method,
        COUNT(*) as payment_count
    FROM TopProducts tp
    JOIN OrderItems oi ON tp.name = (SELECT name FROM Products WHERE product_id = oi.product_id)
    JOIN Orders o ON oi.order_id = o.order_id
    JOIN Payments pym ON o.order_id = pym.order_id
    GROUP BY tp.name, pym.payment_method
)
SELECT 
    tps.name AS top_product,
    pm.payment_method,
    COUNT(*) as total_payments
FROM PaymentStats pm
JOIN TopProducts tps ON pm.name = tps.name
GROUP BY pm.payment_method, tps.name
ORDER BY total_payments DESC;