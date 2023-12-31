from google.cloud import bigquery
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./hale-carport-304214-d9b788ff294c.json"


# create function get datarame for a country_code
POPULATION_PER_COUNTRY = {
    'US': 340090940,
    'FR': 67081000,
    'MG': 29680000,
    'GB': 66020000,
    'CN': 1409517397
}

CONSTANT_FACTOR = 1000000


def get_country_data(country_code):
    # connect to big query and load the data and use json credentials
    client = bigquery.Client()
    # Perform a query.
    QUERY = (
        'SELECT * FROM `hale-carport-304214.worldwide_covid19_after_2020.worldwide_covid19_after_2020` WHERE country_code = "' +
        country_code + '" ORDER BY date ASC'
    )
    result = client.query(QUERY).to_dataframe()  # API request
    # transform the result into a dataframe
    dataframe = pd.DataFrame(result)
    # convert the date column to datetime type
    dataframe['date'] = pd.to_datetime(dataframe['date'])
    # get the dataframe for the country
    country = dataframe
    # replace all null values with 0
    country['new_confirmed'] = country['new_confirmed'].fillna(0).astype(int)
    country['new_deceased'] = country['new_deceased'].fillna(0).astype(int)
    country['new_tested'] = country['new_tested'].fillna(0).astype(int)
    country['new_recovered'] = country['new_recovered'].fillna(0).astype(int)

    # convert data into int type
    # country['new_confirmed'] = country['new_confirmed'].astype(int)
    # country['new_deceased'] = country['new_deceased'].astype(int)
    # get the monthly data for the country
    country_monthly_data = country.groupby(pd.Grouper(
        key='date', freq='M')).agg({'new_confirmed': 'sum', 'new_deceased': 'sum', 'new_tested': 'sum', 'new_recovered': 'sum'}).reset_index()
    # Calculate recovery rate with condition to handle division by zero
    country_monthly_data['recovery_rate'] = np.where(
        country_monthly_data['new_confirmed'] == 0, 1, 1 - (country_monthly_data['new_deceased'] / country_monthly_data['new_confirmed']))

    # country_monthly_data['recovery_rate'] = country_monthly_data.apply(
    #     lambda row: 100 if row['new_deceased'] == 0 else row['recovery_rate'], axis=1)
    # delete all rows with new_confirmed = 0 and new_deceased = 0
    country_monthly_data = country_monthly_data[country_monthly_data['new_confirmed'] != 0]

    # ratio the recovery rate to the population
    country_monthly_data['recovery_rate'] = (country_monthly_data['recovery_rate'] *
                                             CONSTANT_FACTOR) / POPULATION_PER_COUNTRY[country_code]

    # export the monthly_data to a csv file inside CSV folder
    country_monthly_data.to_csv(
        './CSV/' + country_code + '_monthly_data.csv', index=False)
    return country_monthly_data


# function
if __name__ == "__main__":
    # define an array of country codes
    country_codes = ['US', 'FR', 'MG', 'GB', 'CN']
    # create a dataframe for each country and plot all the recovery rates on the same graph
    for country_code in country_codes:
        country_monthly_data = get_country_data(country_code)
        plt.plot(country_monthly_data['date'],
                 country_monthly_data['recovery_rate'],
                 label=country_code, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Recovery Rate')
    plt.legend()
    plt.show()
