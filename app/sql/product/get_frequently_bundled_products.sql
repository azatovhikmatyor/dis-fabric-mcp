;WITH cte1 AS (
	SELECT DISTINCT INVOICECODE
	FROM ddidatawarehouse.INVOICEDETAIL
	WHERE PRODUCTCODE = ?
)
, cte2 AS (
	SELECT 
		invd.INVOICECODE,
		invd.INVOICEDETAILID,
		CAST(invd.LINENUM AS INT) AS LINENUM,
		invd.PRODUCTCODE
	FROM ddidatawarehouse.INVOICEDETAIL AS invd
	JOIN cte1
		ON cte1.INVOICECODE = invd.INVOICECODE
	WHERE PRODUCTCODE <> ?
)
, inv_cnt AS (
	SELECT COUNT(DISTINCT INVOICECODE) AS cnt FROM cte2
), cte3 AS (
	SELECT TOP 10
		PRODUCTCODE,
		COUNT(PRODUCTCODE) AS cnt,
		inv_cnt.cnt AS total_inv_cnt,
		COUNT(PRODUCTCODE) * 100.0 / inv_cnt.cnt AS perc
	FROM cte2, inv_cnt
	GROUP BY PRODUCTCODE, inv_cnt.cnt
	ORDER BY perc DESC
)
SELECT
	cte3.PRODUCTCODE AS ProductCode,
	p.PRODUCTDESC AS ProductDescription,
	cte3.perc AS PercentageOfInvoicesContainTheProduct,
	cte3.cnt AS ProductCount,
	cte3.total_inv_cnt AS NumberOfUniqueInvoices
FROM cte3
JOIN ddidatawarehouse.PRODUCT AS p
	ON cte3.PRODUCTCODE = p.PRODUCTCODE
ORDER BY PercentageOfInvoicesContainTheProduct DESC;