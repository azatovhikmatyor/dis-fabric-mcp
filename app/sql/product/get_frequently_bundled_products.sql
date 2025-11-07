SELECT 
    p.product_id,
    p.product_name,
    COUNT(*) AS bought_together_count
FROM fact_sales fs
JOIN fact_sales fs2
    ON fs.order_id = fs2.order_id
    AND fs2.product_id <> ?   -- exclude the given product itself
JOIN dim_product p
    ON fs2.product_id = p.product_id
WHERE fs.product_id = ?
GROUP BY p.product_id, p.product_name
HAVING COUNT(*) > 1
ORDER BY bought_together_count DESC;