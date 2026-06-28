{{config(materialized='table')}}

SELECT c.customer_state,
      format_timestamp('%Y-%m',o.order_purchase_timestamp) as year_month,
      round(sum(payment_value),2) as orders_value,
      round(avg(payment_value),2) as avg_order_price,
      count(distinct o.order_id) as total_orders
FROM {{ref('orders_silver')}} o
join {{ref('order_payments_silver')}} op
  on o.order_id = op.order_id
join {{ref('customers_silver')}} c
  on o.customer_id = c.customer_id 
group by c.customer_state,year_month