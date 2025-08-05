WITH top_customers AS (
  SELECT customer_id, COUNT(*) AS num_orders
  FROM orders
  GROUP BY customer_id
  ORDER BY num_orders DESC
  LIMIT 5
), customer_order_items AS (
  SELECT co.customer_id, oit.product_id, SUM(oit.quantity) AS total_quantity
  FROM (
    SELECT order_id, customer_id
    FROM orders
    JOIN top_customers tc ON orders.customer_id = tc.customer_id
  ) co
  JOIN orderitems oit ON co.order_id = oit.order_id
  GROUP BY co.customer_id, oit.product_id
), stock_levels AS (
  SELECT product_id, stock_qty FROM products
)
SELECT soi.product_name, soi.total_quantity, s.stock_qty
FROM (
  SELECT p.name AS product_name, coo.product_id, coo.total_quantity
  FROM customer_order_items coo
  JOIN products p ON coo.product_id = p.product_id
) soi
JOIN stock_levels s ON soi.product_id = s.product_id
ORDER BY soi.total_quantity DESC, s.stock_qty ASC;