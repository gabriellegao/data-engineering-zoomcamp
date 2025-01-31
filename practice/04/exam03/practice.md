# 选择题
1. B
2. B
3. C

# 填空题
1. relationships
2. dbt.date_trunc("month", field)
3. 设置的范围内

# 简答题
1. 数据存储类型，ephemeral暂时存在，view 在table上以query为基础新建的表，但这个表并不是永久存储的表格，table是永久存储的表格，incremental用于不断添加新数据
2. 用source先把各个数据库的数据提取到dbt内，再用ref一一引用

# 代码题
3. 需要用到的command：dbt build