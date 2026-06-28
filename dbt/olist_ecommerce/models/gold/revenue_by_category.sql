{{config(materialized='table')}}

SELECT 
      product_category_name_english,
      format_timestamp('%Y-%m',o.order_purchase_timestamp) as year_month,
      round(sum(oi.price),2) as orders_value,
      round(avg(oi.price),2) as avg_order_price,
      count(distinct o.order_id) as total_orders
FROM {{ref('orders_silver')}} o
join {{ref ('order_items_silver')}} oi
  on o.order_id = oi.order_id
join {{ref('products_silver')}} p 
  on oi.product_id = p.product_id
join {{ref('product_category_translations')}} pct
   on p.product_category_name = pct.product_category_name_english
group by pct.product_category_name_english,year_month