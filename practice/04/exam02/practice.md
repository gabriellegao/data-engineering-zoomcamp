# 选择题
1. D
2. B
3. D

# 填空题
1. 外部table(不确定)
2. csv
3. materialization

# 简答题
1. ref：引用内部数据
source: source('staging','external_green_tripdata') 拿着个举例，staging是指这个sql file存储的位置，external_green_tripdata是外部表的名词, 这个也跟schema.yaml有联动性

2.
- unique:
  severity: warn

# 实践题
1.  
{{ config(materialized='table') }}

select 
pickup_datetime,
-- Revenue Calculation
sum(total_revenue) as daily_total_revenue,

-- Distance Calculation
avg(trip_distance) as avg_trip_distance

from {{ ref('fact_trip) }}
group by 1
2.  
models:
- name: dm_daily_trip_metrics
  description:""
  columns:
    - name: daily_total_revenue
      data_type: numeric
      description: ""
      test:
        - not_null:
          serverity: warn
      
    - name: avg_trip_distance
      data_type: numeric
      description: ""
      test:
        - dbt_utils.accepted_range::
          min_value: 0
          inclusive: false

3.  