SELECT 
    o.customer_id,
    p.product_id,
    p.name,
    p.stock_qty,
    SUM(oqi.quantity) AS total_orders
FROM orders o
JOIN OrderItems oqi ON o.order_id = oqi.order_id
JOIN Products p ON oqi.product_id = p.product_id
WHERE o.customer_id IN (
    SELECT customer_id
    FROM Orders
    GROUP BY customer_id
    ORDER BY COUNT(*) DESC
    LIMIT 5
)
GROUP BY o.customer_id, p.product_id, p.name, p.stock_qty
ORDER BY total_orders DESC, p.stock_qty;