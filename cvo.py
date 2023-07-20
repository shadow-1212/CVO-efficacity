import pandas as pd
import matplotlib.pyplot as plt

# Load the data for 2021 and 2022
data_2021 = pd.read_csv('covid19_before_2021.csv')
data_2022 = pd.read_csv('covid19_after_2021.csv')

# Add a 'Year' column to each DataFrame
data_2021['Year'] = 2021
data_2022['Year'] = 2022

# Combine the data for both years
combined_data = pd.concat([data_2021, data_2022], ignore_index=True)

# Convert the 'date' column to datetime type (if not already done)
combined_data['date'] = pd.to_datetime(combined_data['date'])

# Aggregate data on a monthly basis and fill in missing values with 0
monthly_data = combined_data.groupby(
    [pd.Grouper(key='date', freq='M'), 'Year']).sum().fillna(0).reset_index()

# Calculate recovery rate with condition to handle division by zero
monthly_data['recovery_rate'] = monthly_data['new_confirmed'] / \
    monthly_data['new_deceased']
monthly_data['recovery_rate'] = monthly_data.apply(
    lambda row: 100 if row['new_deceased'] == 0 else row['recovery_rate'], axis=1)
# delete all rows with new_confirmed = 0 and new_deceased = 0
monthly_data = monthly_data[monthly_data['new_confirmed'] != 0]
# export the monthly_data to a csv file
monthly_data.to_csv('monthly_data.csv', index=False)

# Data Visualization
plt.figure(figsize=(10, 6))
plt.plot(monthly_data[monthly_data['Year'] == 2021]['date'],
         monthly_data[monthly_data['Year'] == 2021]['recovery_rate'],
         label='Recovery Rate 2021', marker='o')

plt.plot(monthly_data[monthly_data['Year'] == 2022]['date'],
         monthly_data[monthly_data['Year'] == 2022]['recovery_rate'],
         label='Recovery Rate 2022', marker='o')

plt.xlabel('Date')
plt.ylabel('Recovery Rate')
plt.title('COVID-19 Recovery Rate Comparison (2021 vs. 2022)')
plt.legend()
plt.grid(True)
plt.show()
