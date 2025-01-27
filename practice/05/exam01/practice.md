选择题
1. C
2. B
3. B
填空题
1. 重新强制分配，定义numbers of partition layers
2. intermediate stage - reshuffling
3. table （这个我不确定）
简答题
1. UDF 全名叫user defined function，是user自己创作的一个def function. 可以将UDF套用在spark df的其他自带的method中，比如df.withColumn('column_name', udf(params))
2. woker node接受到driver node发送的任务后开始工作，在我的笔记中阐述了两张工作情况，第一个是groupby，先按照partition处理每一层的数据，然后根据他们的groupby keys分类，将分好的数据传输到下一步，并且存在新的partition里，在这个新partition中将数据sort一遍，再将sorted and grouped data 传输到下一个新的partition里，并完成之后的工作
第二种是join，每一行数据都会generate出新的key，然后reshuffling会把拥有相同的key的数据放在新的partition里并传输到下一层，之后将带有相同key的数据合并在同一层
（我不太确定我笔记里面对于groupby and join再worker node里的操作流程是否正确， 如果不正确 请指出来）
代码题
1.  
import pyspark
from pyspark.sql import SparkSession
from datetime import datetime
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql import functions as F 

spark = SparkSession.builder \
    .master('local[*]') \
    .appName('test') \
    .getOrCreate()

df = spark.read.format('csv')..option('header', True).load('taxi_zone_lookup.csv')

df_output = df.filter(df.Zone == 'Airport')

df_output.write.mode('overwrite').svae('output/zones.parquet')
2.  

df_result.write.format('bigquery')\
    .option("table", "data/output") \
    .save()

df = spark.read.parquet("data/input")
df_result = df.groupBy("PULocationID").agg({"fare_amount": "sum"})
df_result.write.format('bigquery')\
    .option("table", "data/output") \
    .save()