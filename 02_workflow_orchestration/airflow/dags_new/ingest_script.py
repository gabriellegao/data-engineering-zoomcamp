from time import time
import pandas as pd
from sqlalchemy import create_engine
import os
import pyarrow.parquet as pq


def ingest_callable(user, password, host, port, db, table_name, parquet_file, csv_file, execution_date):
    print(table_name, parquet_file, execution_date)
    # Connect to postgress server
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # Connect
    engine.connect()

    # Read the Parquet file into a PyArrow Table
    table = pq.read_table(parquet_file)

    df = table.to_pandas()

    # 将 timestamp 列转换为字符串格式
    for col in df.select_dtypes(include=["datetime64[ns]"]).columns:
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Write the table to a CSV file
    df.to_csv(csv_file, index=False)

    # Read data with iterator
    df_iter = pd.read_csv(csv_file, iterator= True, chunksize=100000)
    
    # Read data by chucks
    df = next(df_iter)

    # Create table using first 100k rows
    df.to_sql(con = engine, name = table_name, if_exists = 'replace') 

    # While loop to upload the rest of the data
    while True:
        t_start = time()
        
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df['tpep_pickup_datetime'])
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(con = engine, name = table_name, if_exists = 'append')
        
        t_end = time()
        
        print('inserting data chuck...., take %.3f seconds' % (t_end - t_start))
