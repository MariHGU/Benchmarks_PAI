SELECT 
    p.name AS product_name,
    COUNT(oi.order_item_id) AS units_sold,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY p.name, oi.unit_price
ORDER BY units_sold DESC
LIMIT 1;