WITH most_sold_items AS (
    SELECT product_id AS item, SUM(quantity) AS quantity_sold
    FROM OrderItems
    JOIN Products ON OrderItems.product_id = Products.product_id
    GROUP BY product_id
    ORDER BY quantity_sold DESC
    LIMIT 5
), payments_per_item AS (
    SELECT order_id, payment_method, product_id FROM Payments
    JOIN Orders ON Payments.order_id = Orders.order_id
)
SELECT payment_method, COUNT(DISTINCT item) as count
FROM payments_per_item
JOIN most_sold_items ON payments_per_item.product_id = most_sold_items.item
GROUP BY payment_method
ORDER BY count DESC;