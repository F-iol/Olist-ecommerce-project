{{ config(materialized='table') }}

SELECT 
    c.customer_state, 
    count(distinct o.order_id) as orders_per_state,
    format_timestamp('%Y-%m',o.order_purchase_timestamp) as order_year_month
FROM {{ ref('orders_silver')}} o
join {{ ref('customers_silver')}}  c
  on o.customer_id = c.customer_id
where o.order_status ='delivered'
group by c.customer_state,order_year_month
