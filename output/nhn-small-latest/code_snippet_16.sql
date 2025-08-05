WITH CustomerOrderCount AS (
    SELECT 
        customer_id,
        COUNT(order_id) as order_count
    FROM Orders
    GROUP BY customer_id
    ORDER BY order_count DESC
    LIMIT 5
),
TopCustomerPurchases AS (
    SELECT 
        oi.product_id,
        p.name AS product_name,
        SUM(oi.quantity) as total_quantity_purchased
    FROM OrderItems oi
    JOIN Customers c ON oi.order_id = (SELECT order_id FROM Orders WHERE customer_id = c.customer_id)
    WHERE c.customer_id IN (SELECT customer_id FROM CustomerOrderCount)
    GROUP BY oi.product_id, p.name
),
FinalResult AS (
    SELECT 
        tp.product_id,
        tp.product_name,
        tp.total_quantity_purchased,
        p.stock_qty
    FROM TopCustomerPurchases tp
    JOIN Products p ON tp.product_id = p.product_id
    ORDER BY tp.total_quantity_purchased DESC, p.stock_qty ASC
)
SELECT * FROM FinalResult;