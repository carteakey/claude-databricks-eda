-- Get Databricks Apps cost by app per day for the last 30 days
SELECT
  us.usage_date,
  us.usage_metadata.app_id,
  us.usage_metadata.app_name,
  SUM(us.usage_quantity) AS dbus,
  SUM(us.usage_quantity * lp.pricing.effective_list.default) AS dollars
FROM
  system.billing.usage us
LEFT JOIN system.billing.list_prices lp
  ON lp.sku_name = us.sku_name
  AND us.usage_start_time BETWEEN lp.price_start_time AND COALESCE(lp.price_end_time, NOW())
WHERE
  billing_origin_product = 'APPS'
  AND us.usage_unit = 'DBU'
  AND us.usage_date >= DATE_SUB(NOW(), 30)
GROUP BY ALL
