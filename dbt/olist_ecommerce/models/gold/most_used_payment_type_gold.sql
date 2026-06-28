{{config (materialized='table')}}
SELECT 
    op.payment_type,
    format_timestamp('%Y-%m',o.order_purchase_timestamp) as year_month,
    count(distinct op.order_id) as orders
FROM {{ ref('order_payments_silver')}} op
join {{ref('orders_silver')}} o
  on op.order_id= o.order_id
where o.order_status = 'delivered'
group by op.payment_type,year_month