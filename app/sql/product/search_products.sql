SELECT
    p.product_id,
    p.product_name,
    p.category
FROM dim_product p
WHERE
    LOWER(p.product_name) LIKE ?
    OR LOWER(p.category) LIKE ?
ORDER BY p.product_name;
