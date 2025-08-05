WITH customer_orders AS (
    SELECT customer_id, COUNT(order_id) as total_orders
    FROM Orders
    GROUP BY customer_id
    ORDER BY total_orders DESC
    LIMIT 5
), customer_items AS (
    SELECT oi.customer_id, oi.product_id, SUM(oi.quantity) as quantity
    FROM OrderItems oi
    JOIN Orders o ON oi.order_id = o.order_id
    GROUP BY oi.customer_id, oi.product_id
), stock_levels AS (
    SELECT product_id, stock_qty as current_stock FROM Products
)
SELECT c.first_name, c.last_name, i.product_name, i.category, c.item.quantity, s.current_stock
FROM customer_items c_i
JOIN Customers c ON c_i.customer_id = c.customer_id
JOIN Products i ON c_i.product_id = i.product_id
JOIN stock_levels s ON c_i.product_id = s.product_id
ORDER BY c_i.quantity DESC, s.current_stock ASC;