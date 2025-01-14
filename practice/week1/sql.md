select avg(fare_amount) avg_fare_amount
from ny_taxi
where date(pickup_time) = date(dropoff_date)
group by date(pickup_time), date(dropoff_date)