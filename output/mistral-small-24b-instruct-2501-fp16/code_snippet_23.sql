SELECT
    p.name AS product_name,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.unit_price * oi.quantity) AS total_earnings
FROM
    OrderItems oi
JOIN
    Products p ON oi.product_id = p.product_id
GROUP BY
    p.product_id, p.name
ORDER BY
    total_quantity_sold DESC
LIMIT 1;