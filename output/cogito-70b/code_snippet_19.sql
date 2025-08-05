SELECT 
    p.name,
    SUM(oi.quantity) as total_quantity_sold,
    SUM(oi.unit_price * oi.quantity) as total_earnings
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.name
ORDER BY total_quantity_sold DESC
LIMIT 1;