-- 设定这个sql file的文件名为dm_monthly_trip_summary.sql
with trip_data as (
    select *
    from {{ ref('fact_trip') }}
)

select date_trunc('month', pickup_datetime) as pickup_month,
sum(fare_amount) as monthly_total_revenue,
avg(passenger_count) as avg_monthly_passenger_count
from trip_data
group by 1