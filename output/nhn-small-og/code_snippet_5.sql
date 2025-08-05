WITH total_quantities AS (
  SELECT product_id, SUM(quantity) AS total_sold
  FROM orderitems
  GROUP BY product_id
), top_selling_item AS (
  SELECT product_id, total_sold
  FROM total_quantities
  ORDER BY total_sold DESC
  LIMIT 1
)
SELECT p.name, SUM(oit.unit_price * oit.quantity) AS earnings
FROM products p
JOIN top_selling_item tsi ON p.product_id = tsi.product_id
JOIN orderitems oit ON p.product_id = oit.product_id
GROUP BY p.name;