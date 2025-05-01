#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name

    
    parquet_name = "output.parquet"
    os.system(f"curl -o {parquet_name} {url}")
    #
    # df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    # df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")
    # engine.connect()
    df = pd.read_parquet(parquet_name)

    pd.io.sql.get_schema(df, name=table_name, con=engine)

    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')

    chunksize = 100000
    num_chunks = len(df) // chunksize + 1

    for i in range(num_chunks):
        chunk = df.iloc[i*chunksize:(i+1)*chunksize]
        chunk['tpep_pickup_datetime'] = pd.to_datetime(chunk['tpep_pickup_datetime'])
        chunk['tpep_dropoff_datetime'] = pd.to_datetime(chunk['tpep_dropoff_datetime'])
        # Insert into database
        chunk.to_sql(name="table_name", con=engine, if_exists='append')

        print(f"Inserted chunk {i+1} with {len(chunk)} rows")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest data into PostgreSQL")
    parser.add_argument("--user",  help="PostgreSQL username")
    parser.add_argument("--password", help="PostgreSQL password")
    parser.add_argument("--host", help="PostgreSQL host")   
    parser.add_argument("--port", help="PostgreSQL port")
    parser.add_argument("--db", help="PostgreSQL database name")
    parser.add_argument("--table-name", help="PostgreSQL table name")
    parser.add_argument("--url", help="PostgreSQL connection URL")

    args= parser.parse_args()
    main(args)

