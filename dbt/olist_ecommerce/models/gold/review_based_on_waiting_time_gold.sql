{{ config(materialized='table') }}

select 
    format_timestamp('%Y-%m', o.order_purchase_timestamp) order_year_month,
    avg(r.review_score) avg_review_score,
    count(distinct o.order_id) total_orders,
    avg(date_diff(o.order_delivered_customer_date, o.order_purchase_timestamp, day)) avg_delivery_time_days
from {{ ref('order_reviews_silver') }} r
join {{ ref('orders_silver') }} o 
    on r.order_id = o.order_id
where o.order_status = 'delivered'
group by order_year_month