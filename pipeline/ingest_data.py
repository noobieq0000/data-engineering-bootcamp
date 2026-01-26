#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


@click.command()
@click.option(
    "--db-url",
    default="postgresql://root:root@localhost:5432/ny_taxi",
    help="Database connection URL",
    type=str,
)
@click.option(
    "--url",
    default="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz",
    help="CSV file URL",
    type=str,
)
@click.option(
    "--table-name",
    default="yellow_taxi_data",
    help="Table name to insert data into",
    type=str,
)
@click.option(
    "--chunksize",
    default=100_000,
    help="Chunk size for reading CSV",
    type=int,
)
def ingest_data(db_url: str, url: str, table_name: str, chunksize: int) -> None:
    """Ingest NYC taxi data into PostgreSQL database."""
    
    # Create database engine
    engine = create_engine(db_url)
    
    # Define data types
    dtype = {
        "VendorID": "Int64",
        "passenger_count": "Int64",
        "trip_distance": "float64",
        "RatecodeID": "Int64",
        "store_and_fwd_flag": "string",
        "PULocationID": "Int64",
        "DOLocationID": "Int64",
        "payment_type": "Int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
    }
    
    parse_dates = ["tpep_pickup_datetime", "tpep_dropoff_datetime"]
    
    click.echo(f"Reading data from {url}...")
    
    # Read CSV in chunks
    df_iter = pd.read_csv(
        url,
        compression="gzip",
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )
    
    first = True
    total = 0
    
    # Process chunks
    for chunk in tqdm(df_iter):
        if first:
            click.echo(f"Creating table '{table_name}'...")
            chunk.head(0).to_sql(table_name, con=engine, if_exists="replace", index=False)
            first = False
        
        chunk.to_sql(table_name, con=engine, if_exists="append", index=False, method="multi")
        total += len(chunk)
    
    click.echo(f"✓ Successfully ingested {total} rows into '{table_name}'")


if __name__ == "__main__":
    ingest_data()
