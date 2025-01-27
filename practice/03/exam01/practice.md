选择题1.A 2.B 3.A 4.B 5.C
简答题
1.oltp属于日常数据频繁录入数据库，所以数据偏于的normalization, 对于数据的写入速度要求高
olap属于后期分析类，对数据join, 对比要求高，但是录入不高，而且更倾向于denormalization
2.volume配置其实是挂载，在docker内部和local machine都有备份，防止数据丢失，google credential也是同理，将credential备份在两个位置，方便airflow调度任务时，可以顺利连接gsp
代码题
1. 我就不修改整个代码了，只修改schedule_interval
   schedule interval="00 9 * 1-12 1-5"
2. 这道题有两种写法
第一种是将dag设置成def func,在def func内部写好各个任务代码，然后在外部call这个def func，def func里面带variables，但我没想好怎么一个一个读取这三年的文件
第二种就是dag外部写一个list or dict,内部写一个foor loop，然后把日期作为variable一个一个放进去
3. select avg(total_amount)
 from external_yellow_tripdata_partitioned
 where pickup_datetime >= '2023-06-01' and pickup_datetime <='2023-06-30'
 group by year(pickup_datetime), month(pickup_datetime)