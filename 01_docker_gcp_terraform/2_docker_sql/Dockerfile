# 知识点总结：
# 1. ENTRYPOINT: 定义了程序环境, 定义成python,会自动进入到python的环境中; 定义的是bash, 则会进入到bash的环境中。
# 2. 进入到bash的环境中, 需要手动调动python
# 3. Build image docker build -t <container_name> .
# 4. Run image: docker build -it <container_name>


FROM python:3.9

RUN pip install pandas sqlalchemy psycopg2 wget


WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT ["python", "ingest_data.py"]
