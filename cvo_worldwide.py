from google.cloud import bigquery
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# connect to big query and load the data and use json credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./hale-carport-304214-d9b788ff294c.json"
client = bigquery.Client()
# Perform a query.
QUERY = (
    'SELECT * FROM `bigquery-public-data.covid19_open_data.covid19_open_data` cl'
    'WHERE date BETWEEN "2021-01-01" AND "2021-12-31" '
    'AND country_name in ("United States of America","France","Madagascar","United Kingdom","China")'
    'AND date >= "2020-12-31"'
    ' and (CAST(new_tested AS INTEGER) >= CAST(new_confirmed AS INTEGER)  OR (new_tested IS NULL AND (new_confirmed IS NULL or new_confirmed=0))) '
    'order by date asc'
)
query_job = client.query(QUERY)  # API request
data = query_job.to_dataframe()  # Waits for query to finish
# to export the data to a csv file
data.to_csv('covid19_after_2020.csv', index=False)
