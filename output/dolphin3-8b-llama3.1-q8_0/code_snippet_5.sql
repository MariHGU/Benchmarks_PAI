SELECT Payments.payment_method, COUNT(Payments.order_id) AS num_orders 
FROM Payments 
JOIN OrderItems ON Payments.order_id = OrderItems.order_id 
WHERE OrderItems.product_id IN (
    SELECT OrderItems.product_id 
    FROM OrderItems 
    GROUP BY OrderItems.product_id 
    ORDER BY SUM(OrderItems.quantity) DESC 
    LIMIT 5
)
GROUP BY Payments.payment_method 
ORDER BY num_orders DESC;