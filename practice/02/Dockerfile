# 1️⃣ 选择轻量级 Python 3.9
FROM python:3.9-slim

# 2️⃣ 设置工作目录
WORKDIR /opt/airflow

# 3️⃣ 复制依赖文件
COPY requirements.txt .

# 4️⃣ 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 5️⃣ 复制 DAG 代码（如果有）
COPY dags/ ./dags

# 6️⃣ 运行 Airflow Scheduler
ENTRYPOINT ["airflow", "scheduler"]
