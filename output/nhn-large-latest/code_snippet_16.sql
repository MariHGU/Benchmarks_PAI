WITH MostSold AS (
    SELECT 
        product_id,
        SUM(quantity) AS total_quantity,
        SUM(unit_price * quantity) AS total_revenue
    FROM OrderItems
    GROUP BY product_id
)
SELECT 
    p.product_id,
    p.name AS product_name,
    ms.total_quantity,
    ms.total_revenue
FROM MostSold ms
JOIN Products p ON ms.product_id = p.product_id
ORDER BY ms.total_quantity DESC
LIMIT 1;