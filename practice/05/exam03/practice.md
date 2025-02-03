# 理论题
1. map主要是将每一行数据放到def fun里，然后输出结果。flatmap我记得是将几行数据组合起来，再套入到def func里
   reduceByKey是从上一步map()提取出每一个layer/partition的composite key and value分别提取出来，再分成左右数据进行计算
   groupByKey不知道是什么
2.  
```bash
mkdir -p my_directory
wget my_file.gz
tar xzfv my_file.gz

if [ $? -ne 0 ]; then
  echo "Error unzip the file!"
fi
# 这道题我不确定，请给出你的答案
```
3. executor_memory应该值得是driver node的memory资源配置，其他的两个不知道。在提交spark submit时，可以输入--jars xxx来下载或者配置jar

# 代码题
第三问：这道题我假定一个cluster
```bash
URL="spark://code-03-master-url.internal:7077"
spark-submit \
    --master="${URL}" \
    --executor_memory = "4 GB" \
    --jars=spark-bigquery-latest_2.12.jar \
    process_data.py \

```