# 选择题
1. C（如果这个的英文翻译是offset）
2. B
3. A
4. B

# 简答题
1. 消息是通过key分类再流入不同的partitions，using hash to determine which partition that key should go to.
2. 可以用windows来分区messages，可以分时间来分析数据，比如uber可以用这个message window来计算每个小时的打车人数
3. (这个概念我不是很熟悉，所以接下来的回答算是我盲猜，你可以等会儿给我一个比较正确的结束)，首先每条数据都是带有key，offset，partition and timestamp，而这些数据造就了每条数据的独立性，使得每个数据即使可能value一样，也不会重复

# 填空题
1. 方便数据导入，运行。使多个node可以同时处理小量的数据，加快数据处理的效率，更高效的使用资源
2. seconds or minutes
3. shut down all the services
4. 过滤掉不需要的数据（不确定）

# 代码题
5.  
df_stream = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", ["rides_csv",'topic1','topic2']) \
    .load()
