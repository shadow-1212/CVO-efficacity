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
    'SELECT * FROM `hale-carport-304214.worldwide_covid19_after_2020.worldwide_covid19_after_2020` '
)
data = client.query(QUERY).to_dataframe  # API request
dataframe = pd.DataFrame(data)
# export the data to a csv file
# Aggregate data on a monthly basis  by country and fill in missing values with 0
# monthly_data = data.groupby(
#     [pd.Grouper(key='date', freq='M'), 'country_name']).sum().fillna(0).reset_index()
# # Calculate recovery rate with condition to handle division by zero
# monthly_data['recovery_rate'] = monthly_data['new_confirmed'] / \
#     monthly_data['new_deceased']
# monthly_data['recovery_rate'] = monthly_data.apply(
#     lambda row: 100 if row['new_deceased'] == 0 else row['recovery_rate'], axis=1)
# # delete all rows with new_confirmed = 0 and new_deceased = 0
# monthly_data = monthly_data[monthly_data['new_confirmed'] != 0]
# # export the monthly_data to a csv file
# monthly_data.to_csv('monthly_data.csv', index=False)
