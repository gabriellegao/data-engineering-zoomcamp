### 实践题第二问
{{ config(materialized='table') }}


    select 
    -- Reveneue grouping 
    pickup_zone as revenue_zone,
    {{ dbt.date_trunc("month", "pickup_datetime") }} as revenue_month, 
    {{ dbt.date_trunc("week", "pickup_datetime") }} as revenue_week, 

    service_type, 
    sum(total_amount) as revenue_weeklyly_total_amount,

    -- Additional calculations
    count(tripid) as total_weekly_trips

    from {{ source('core','fact_trip') }}
    group by 1,2,3,4


### 实践题第三问
models:
  - name: dm_weekly_zone_revenue
    description: ""
    columns:
      - name: trip_account
        data_type: int64
        description: ""
        tests:
            - not_null:
                severity: warn
          

