SELECT 
    oi.product_id,
    p.name AS product_name,
    SUM(oi.quantity) as total_sold_quantity,
    (SUM(oi.quantity) * AVG(oi.unit_price)) as total_earnings
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
GROUP BY oi.product_id, p.name
ORDER BY total_sold_quantity DESC
LIMIT 1;