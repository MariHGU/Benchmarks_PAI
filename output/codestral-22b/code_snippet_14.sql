SELECT c.first_name, c.last_name, p.name AS product_name, SUM(oi.quantity) AS total_purchased, pr.stock_qty
FROM Customers AS c
JOIN Orders AS o ON c.customer_id = o.customer_id
JOIN OrderItems AS oi ON o.order_id = oi.order_id
JOIN Products AS p ON oi.product_id = p.product_id
WHERE c.customer_id IN (
    SELECT customer_id
    FROM Orders
    GROUP BY customer_id
    ORDER BY COUNT(order_id) DESC
    LIMIT 5
)
GROUP BY c.customer_id, oi.product_id
ORDER BY pr.stock_qty ASC;