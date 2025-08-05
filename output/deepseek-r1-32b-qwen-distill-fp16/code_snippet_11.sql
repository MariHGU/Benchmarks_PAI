WITH MostSoldItem AS (
    SELECT 
        product_id,
        SUM(quantity) as total_sold,
        SUM(quantity * unit_price) as total_revenue
    FROM 
        OrderItems
    GROUP BY 
        product_id
    ORDER BY 
        total_sold DESC, total_revenue DESC
)
SELECT 
    msi.product_id,
    p.name AS product_name,
    msi.total_sold,
    msi.total_revenue
FROM 
    MostSoldItem msi
JOIN 
    Products p ON msi.product_id = p.product_id
LIMIT 1;