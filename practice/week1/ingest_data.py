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
    database = params.database
    table_name = params.table_name
    url = params.url

    engine = create_engine(f'postgressql://{user}:{password}@{host}:{port}/{database}')
    engine.connect()

    file_path_list = ['2023-01', '2023-02', '2023-03']

    csv_file_path = dict()
    for path in file_path_list:
        # full path example: https://example.com/data_2023-01.csv.gz
        csv_file_path[path] = f'{url}_data_{path}.csv'
        os.system(f'wget {url}_data_{path}.csv.gz')
        os.system(f'gzip -d {url}_data_{path}.csv.gz')
    
    for key, value in csv_file_path.items():
        subtable_name = f'{table_name}_{key}'
        # Assume each file has over 100000 rows, I'd like to read it by chuck
        df_iter = pd.read_csv(value, iterator=True, chuncksize = 100000)
        df = next(df_iter)
        df.to_sql(con = engine, name = subtable_name, if_exists = 'replace')
        while True:
            df = next(df_iter)
            df.to_sql(con = engine, name = subtable_name, if_exists = 'append')



if __name__ == "__mian__":
    parser = argparse.ArgumentParser(description='Ingest Data')

    parser.add_argument('--user')
    parser.add_argument('--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--databse')
    # Assume prefix of table looks like ny_taxi
    parser.add_argument('--table_name')
    # Assume the prefix of url input looks like https://example.com/
    parser.add_argument('--url')
    
    args = parser.parse_args()

    main(args)


