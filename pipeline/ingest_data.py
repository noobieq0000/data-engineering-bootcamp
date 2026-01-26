#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")



prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
url = prefix + "yellow_tripdata_2021-01.csv.gz"

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


# In[7]:


df_iter = pd.read_csv(
    url,
    compression="gzip",
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100_000
)

first_chunk = next(df_iter)
first_chunk.shape


# In[8]:


from tqdm.auto import tqdm

table_name = "yellow_taxi_data"

# 1) Create table (schema only)
first_chunk.head(0).to_sql(
    name=table_name,
    con=engine,
    if_exists="replace",
    index=False
)

# 2) Insert first chunk
first_chunk.to_sql(
    name=table_name,
    con=engine,
    if_exists="append",
    index=False,
    method="multi"
)
print("Inserted first chunk:", len(first_chunk))

# 3) Insert remaining chunks
for chunk in tqdm(df_iter):
    chunk.to_sql(
        name=table_name,
        con=engine,
        if_exists="append",
        index=False,
        method="multi"
    )

print("Done")


# In[10]:


pd.read_sql("select count(*) as c from yellow_taxi_data", con=engine)


# In[11]:


from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")

prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
url = prefix + "yellow_tripdata_2021-01.csv.gz"

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

df_iter = pd.read_csv(
    url,
    compression="gzip",
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100_000
)

first_chunk = next(df_iter)

# create table
first_chunk.head(0).to_sql("yellow_taxi_data", con=engine, if_exists="replace", index=False)

# insert first 100k rows
first_chunk.to_sql("yellow_taxi_data", con=engine, if_exists="append", index=False, method="multi")

# show count (IMPORTANT: no semicolon at the end)
pd.read_sql("select count(*) as c from yellow_taxi_data", con=engine)


# In[12]:


# create table
first_chunk.head(0).to_sql("yellow_taxi_data", con=engine, if_exists="replace", index=False)

# insert first 100k rows
first_chunk.to_sql("yellow_taxi_data", con=engine, if_exists="append", index=False, method="multi")
print("Inserted first chunk:", len(first_chunk))


# In[13]:


pd.read_sql("select count(*) as c from yellow_taxi_data", con=engine)


# In[ ]:


from sqlalchemy import create_engine
import pandas as pd
from tqdm.auto import tqdm

engine = create_engine("postgresql://root:root@localhost:5432/ny_taxi")

prefix = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
url = prefix + "yellow_tripdata_2021-01.csv.gz"

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

df_iter = pd.read_csv(
    url,
    compression="gzip",
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100_000,
)

first = True
total = 0

for chunk in tqdm(df_iter):
    if first:
        chunk.head(0).to_sql("yellow_taxi_data", con=engine, if_exists="replace", index=False)
        first = False

    chunk.to_sql("yellow_taxi_data", con=engine, if_exists="append", index=False, method="multi")
    total += len(chunk)

total


# In[ ]:




