WITH top_sold AS (
  SELECT product_id, SUM(quantity) AS sold_qty
  FROM OrderItems
  GROUP BY product_id
  ORDER BY sold_qty DESC
  LIMIT 5
)

SELECT o.payment_method, COUNT(*) AS payment_count
FROM Payments o
JOIN Orders r ON o.order_id = r.order_id
WHERE r.product_id IN (SELECT product_id FROM top_sold)
GROUP BY o.payment_method
ORDER BY payment_count DESC;