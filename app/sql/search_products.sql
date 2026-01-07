SELECT
    p.product_id,
    p.product_code,
    p.product_name,
    p.brand,
    p.category
FROM dim_product p
WHERE
    LOWER(p.product_name) LIKE :query
    OR LOWER(p.brand) LIKE :query
    OR LOWER(p.category) LIKE :query
    OR LOWER(p.description) LIKE :query
ORDER BY p.product_name;
