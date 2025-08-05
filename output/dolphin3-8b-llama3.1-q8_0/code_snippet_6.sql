SELECT Products.name, COUNT(OrderItems.order_item_id) AS num_items_purchased, Products.stock_qty 
FROM OrderItems 
JOIN Orders ON OrderItems.order_id = Orders.order_id 
JOIN Customers ON Orders.customer_id = Customers.customer_id 
JOIN Products ON OrderItems.product_id = Products.product_id 
WHERE Orders.order_date IN (
    SELECT Orders.order_date 
    FROM Orders 
    GROUP BY Orders.customer_id 
    ORDER BY COUNT(Orders.order_id) DESC 
    LIMIT 5
)
GROUP BY Products.name, Products.stock_qty 
ORDER BY num_items_purchased DESC, Products.stock_qty ASC;