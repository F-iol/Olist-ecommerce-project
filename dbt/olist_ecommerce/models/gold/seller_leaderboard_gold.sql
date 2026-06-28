{{config(materialized='table')}}

SELECT 
    concat(
      "Seller_",left(s.seller_id,3),' (',
      s.seller_city,'-',s.seller_state,')'
    ) as seller_city_state, 
    round(sum(oi.price),2) as total_seller_revenue,
    round(sum(oi.freight_value),2) as total_freight_value ,
    count(distinct oi.order_id) as total_sell_orders
FROM {{ref('sellers_silver')}} s
join {{ref("order_items_silver")}} oi
  on s.seller_id = oi.seller_id
group by 1