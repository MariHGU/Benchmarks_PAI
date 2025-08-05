SELECT OrderItems.product_id, SUM(OrderItems.quantity * OrderItems.unit_price) AS total_earnings 
FROM OrderItems 
GROUP BY OrderItems.product_id 
ORDER BY SUM(OrderItems.quantity) DESC 
LIMIT 1;