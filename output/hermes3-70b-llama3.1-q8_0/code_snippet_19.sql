SELECT c.customer_id, c.first_name, c.last_name, p.product_id, p.name, 
       SUM(oi.quantity) AS total_quantity_purchased, p.stock_qty
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN OrderItems oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
WHERE c.customer_id IN (
    SELECT customer_id
    FROM Orders
    GROUP BY customer_id
    ORDER BY COUNT(*) DESC
    LIMIT 5
)
GROUP BY c.customer_id, c.first_name, c.last_name, p.product_id, p.name, p.stock_qty
HAVING SUM(oi.quantity) = (
    SELECT MAX(total_quantity)
    FROM (
        SELECT SUM(oi2.quantity) AS total_quantity
        FROM OrderItems oi2
        WHERE oi2.product_id = p.product_id AND oi2.order_id IN (
            SELECT order_id
            FROM Orders
            WHERE customer_id = c.customer_id
        )
        GROUP BY oi2.product_id
    ) AS subquery
)
ORDER BY p.stock_qty ASC;