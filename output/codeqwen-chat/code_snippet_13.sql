WITH customer_orders AS (
  SELECT customer_id, COUNT(order_id) AS order_count
  FROM Orders
  GROUP BY customer_id
  ORDER BY order_count DESC
  LIMIT 5
),

customer_items AS (
  SELECT o.customer_id, o.product_id, p.name AS product_name, SUM(oi.quantity) AS total_purchased
  FROM Orders o
  JOIN OrderItems oi ON o.order_id = oi.order_id
  JOIN Products p ON oi.product_id = p.product_id
  WHERE o.customer_id IN (SELECT customer_id FROM customer_orders)
  GROUP BY o.customer_id, o.product_id, p.name
),

sorted_items AS (
  SELECT product_id, product_name, total_purchased, stock_qty
  FROM Products p
  JOIN customer_items ci ON p.product_id = ci.product_id
  ORDER BY stock_qty ASC
)

SELECT customer_id, c.first_name, c.last_name, si.product_id, si.product_name, si.total_purchased, si.stock_qty
FROM Customers c
JOIN sorted_items si ON c.customer_id = si.customer_id
ORDER BY si.stock_qty ASC;