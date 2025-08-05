SELECT product_id AS product, SUM(quantity) AS quantity_sold, SUM(unit_price * quantity) AS total_revenue
FROM OrderItems
JOIN Products ON OrderItems.product_id = Products.product_id
GROUP BY product_id
ORDER BY quantity_sold DESC
LIMIT 1;