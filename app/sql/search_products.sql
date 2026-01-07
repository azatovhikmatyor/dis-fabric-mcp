SELECT
    p.product_id,
    p.product_name,
    p.category
FROM dim_product p
WHERE
    LOWER(p.product_name) LIKE :query
    OR LOWER(p.category) LIKE :query
ORDER BY p.product_name;
