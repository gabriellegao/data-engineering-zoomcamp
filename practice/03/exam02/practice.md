# 选择题
1. C
2. A
3. B
4. B
5. A

# 简答题
1. 不知道airflow能不能根据任务分配资源比如cpu memory之类的，如果可以的话，给这个时耗长的task多分配些资源，
或者将这个大的任务split up成一个一个小任务，外加上优化代码
2. 在service全部启动后，直接可以连接gcp，如果没有的话 就链接不上

# 代码题
1. 现在我的sourceUris是这样的：[f"gs://{BUCKET}/{color}/{color}_tripdata_2019-01.parquet"]
如果我想加载多个时间段的文件，我可以使用jinjia的execution_datetime
如果担心多余的/，maybe可以使用real path, 类似os.path.realpath(xxxx),我不知道针对于gs的real path methods是什么
2. 在dag python script最下面规划任务运行顺序那儿可以标明：task_A >> task_B
3. 
```python
year_month_lst = ['2019-01', '2019-02', '2019-03', '2019-04']

for year_month in year_month_lst:
    gcs_2_bq_ext_task = BigQueryCreateExternalTableOperator(
        task_id="gcs_2_bq_ext_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": f"external_{color}_tripdata_{year_month}",
            },
            "externalDataConfiguration": {
                "autodect": True,
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/{color}/{color}_tripdata_{year_month}.parquet"],
            }
        })
```
或者吧year_month存在iterator里，用next()一个一个call iterator, 然后吧当前的year_month放进tableId and sourceUris.
还有种写法是在dag外部写一个DAG和一个def，将year_month_lst作为parameters导入到task里，同样是用for loop or iterator to extract values. 