WITH top_selling_items AS (
  SELECT product_id, SUM(quantity) AS total_sold
  FROM orderitems
  GROUP BY product_id
  ORDER BY total_sold DESC
  LIMIT 5
), payments_per_item AS (
  SELECT p.product_id, payment_method, COUNT(*) AS num_payments
  FROM orderitems oit
  JOIN orders o ON oit.order_id = o.order_id
  JOIN payments p ON o.order_id = p.order_id
  WHERE oit.product_id IN (SELECT product_id FROM top_selling_items)
  GROUP BY p.product_id, payment_method
), most_used_payment AS (
  SELECT payment_method, SUM(num_payments) AS total
  FROM payments_per_item
  GROUP BY payment_method
  ORDER BY total DESC
  LIMIT 1
)
SELECT mup.payment_method, p.name, COUNT(*) AS num_occurrences
FROM most_used_payment mup
JOIN products p ON mup.total = (
  SELECT SUM(num_payments) FROM payments_per_item WHERE payment_method = mup.payment_method
)
GROUP BY mup.payment_method, p.name
ORDER BY num_occurrences DESC;