-- Adjusted SQL Query for calculating deviations
SELECT 
    time,
    today,
    yesterday,
    same_day_last_week,
    avg_last_week,
    avg_last_month,
    (today - avg_last_week) AS deviation_from_avg_last_week,
    (today - avg_last_month) AS deviation_from_avg_last_month
FROM 
    checkout_data
ORDER BY 
    time;
import matplotlib.pyplot as plt

# Preparing data for the plot
time = data1['time']
today = data1['today']
avg_last_week = data1['avg_last_week']
avg_last_month = data1['avg_last_month']
deviation_from_avg_last_week = data1['deviation_from_avg_last_week']
deviation_from_avg_last_month = data1['deviation_from_avg_last_month']

# Creating the plot
plt.figure(figsize=(14, 7))

# Plotting today's values
plt.plot(time, today, label='Today', marker='o')

# Plotting the average of last week and last month
plt.plot(time, avg_last_week, label='Avg Last Week', linestyle='--')
plt.plot(time, avg_last_month, label='Avg Last Month', linestyle='--')

# Highlighting anomalies
plt.fill_between(time, today, avg_last_week, 
                 where=abs(deviation_from_avg_last_week) > 2 * deviation_from_avg_last_week.std(), 
                 color='red', alpha=0.3, label='Anomalies Last Week')
plt.fill_between(time, today, avg_last_month, 
                 where=abs(deviation_from_avg_last_month) > 2 * deviation_from_avg_last_month.std(), 
                 color='orange', alpha=0.3, label='Anomalies Last Month')

# Plot settings
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Checkout Data Analysis with Anomalies')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Displaying the plot
plt.show()
import matplotlib.pyplot as plt

# Creating the plot again without fill_between
plt.figure(figsize=(14, 7))

# Plotting today's values
plt.plot(time, today, label='Today', marker='o')

# Plotting the average of last week and last month
plt.plot(time, avg_last_week, label='Avg Last Week', linestyle='--')
plt.plot(time, avg_last_month, label='Avg Last Month', linestyle='--')

# Highlighting anomalies with red and orange points
anomalies_last_week = data1[abs(data1['deviation_from_avg_last_week']) > 2 * deviation_from_avg_last_week.std()]
anomalies_last_month = data1[abs(data1['deviation_from_avg_last_month']) > 2 * deviation_from_avg_last_month.std()]

plt.scatter(anomalies_last_week['time'], anomalies_last_week['today'], color='red', label='Anomalies Last Week')
plt.scatter(anomalies_last_month['time'], anomalies_last_month['today'], color='orange', label='Anomalies Last Month')

# Plot settings
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('Checkout Data Analysis with Anomalies')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)

# Displaying the plot
plt.show()
