
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine
import os
import gzip
import shutil

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name
    
    # Connect to postgress server
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    # Connect
    engine.connect()

    # Path to gz file
    gz_file_path = "output_csv.gz"

    # Path to csv file
    csv_file_path = "output_csv.csv"

    # Download csv file in .gz
    os.system(f'wget {url} -O {gz_file_path}')

    # Unzip gz file and convert it to csv file
    with gzip.open(gz_file_path, 'rb') as gz_file:
        with open(csv_file_path, 'wb') as csv_file:
            shutil.copyfileobj(gz_file, csv_file)
    
    
    df_iter = pd.read_csv(csv_file_path, iterator= True, chunksize=100000)
    
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

# 当脚本被直接运行的时候，main function才会跑起来
# 如果作为模块导入到其他py script时，以下的代码不会被运行
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgress')

    parser.add_argument('--user', help = 'user name')
    parser.add_argument('--password', help = 'password')
    parser.add_argument('--host', help = 'host')
    parser.add_argument('--port', help = 'port')
    parser.add_argument('--db', help = 'database name')
    parser.add_argument('--table_name', help ='table name')
    parser.add_argument('--url', help = 'csv url')

    args = parser.parse_args()

    main(args)