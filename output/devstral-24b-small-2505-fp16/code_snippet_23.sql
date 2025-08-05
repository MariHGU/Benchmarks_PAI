WITH TopCustomers AS (
  SELECT c.customer_id,
         COUNT(o.order_id) AS order_count
  FROM Customers c
  JOIN Orders o ON c.customer_id = o.customer_id
  GROUP BY c.customer_id
  ORDER BY order_count DESC
  LIMIT 5
)
SELECT p.name AS product_name, SUM(oi.quantity) AS total_quantity_purchased, p.stock_qty
FROM OrderItems oi
JOIN Products p ON oi.product_id = p.product_id
JOIN Orders o ON oi.order_id = o.order_id
JOIN TopCustomers tc ON o.customer_id = tc.customer_id
GROUP BY p.name, p.stock_qty
ORDER BY total_quantity_purchased DESC, p.stock_qty ASC;