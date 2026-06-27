{{ config(materialized='table')}}

select 
    pct.product_category_name_english,
    round(avg(r.review_score),2) avg_review_score,
    count(distinct o.order_id) total_orders
from {{ref('order_reviews_silver')}} r
join {{ ref('orders_silver')}} o
    on r.order_id = o.order_id
join {{ ref('order_items_silver')}} oi
    on o.order_id = oi.order_id
join {{ ref('products_silver')}} p 
    on oi.product_id = p.product_id
join {{ref('product_category_translations')}} pct
    on p.product_category_name = pct.product_category_name
where o.order_status = 'delivered'
group by pct.product_category_name_english