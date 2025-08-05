SELECT product_id, COUNT(*) AS sales_volume
FROM sales
GROUP BY product_id
ORDER BY sales_volume DESC
LIMIT 5;