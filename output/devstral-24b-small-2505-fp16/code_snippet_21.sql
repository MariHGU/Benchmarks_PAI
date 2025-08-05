WITH TopSoldItems AS (
  SELECT p.name AS product_name,
         SUM(oi.quantity) AS total_quantity_sold
  FROM OrderItems oi
  JOIN Products p ON oi.product_id = p.product_id
  GROUP BY p.name
  ORDER BY total_quantity_sold DESC
  LIMIT 5
)
SELECT pm.payment_method, COUNT(*) AS payment_count
FROM Payments pm
JOIN Orders o ON pm.order_id = o.order_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN TopSoldItems tsi ON oi.product_id = (SELECT product_id FROM Products WHERE name = tsi.product_name)
GROUP BY pm.payment_method
ORDER BY payment_count DESC
LIMIT 1;