-- Create tables for checkout data
CREATE TABLE checkout_data_1 (
    time VARCHAR(3),
    today INT,
    yesterday INT,
    same_day_last_week INT,
    avg_last_week FLOAT,
    avg_last_month FLOAT
);

CREATE TABLE checkout_data_2 (
    time VARCHAR(3),
    today INT,
    yesterday INT,
    same_day_last_week INT,
    avg_last_week FLOAT,
    avg_last_month FLOAT
);

-- Create tables for transaction data
CREATE TABLE transactions_1 (
    timestamp TEXT,
    status TEXT,
    amount REAL
);

CREATE TABLE transactions_2 (
    timestamp TEXT,
    status TEXT,
    amount REAL
);
-- Insert data into checkout_data_1 (example)
INSERT INTO checkout_data_1 VALUES ('00h', 9, 12, 11, 6.42, 4.85);
INSERT INTO checkout_data_1 VALUES ('01h', 3, 5, 1, 1.85, 1.92);
-- Continue inserting the rest of the data...

-- Insert data into checkout_data_2 (example)
INSERT INTO checkout_data_2 VALUES ('00h', 6, 9, 5, 5.00, 4.92);
INSERT INTO checkout_data_2 VALUES ('01h', 3, 3, 2, 2.00, 1.92);
-- Continue inserting the rest of the data...

-- Insert data into transactions_1 (example)
INSERT INTO transactions_1 VALUES ('2024-07-30 10:00:00', 'approved', 100.0);
INSERT INTO transactions_1 VALUES ('2024-07-30 10:01:00', 'failed', 50.0);
-- Continue inserting the rest of the data...

-- Insert data into transactions_2 (example)
INSERT INTO transactions_2 VALUES ('2024-07-30 10:03:00', 'approved', 200.0);
INSERT INTO transactions_2 VALUES ('2024-07-30 10:04:00', 'reversed', 100.0);
-- Continue inserting the rest of the data...
-- Calculate deviations from average last week and average last month
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
    checkout_data_1
ORDER BY 
    time;

-- Repeat for checkout_data_2
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
    checkout_data_2
ORDER BY 
    time;
import matplotlib.pyplot as plt

# Prepare data for the plot
time = data1['time']
today = data1['today']
avg_last_week = data1['avg_last_week']
avg_last_month = data1['avg_last_month']
deviation_from_avg_last_week = data1['deviation_from_avg_last_week']
deviation_from_avg_last_month = data1['deviation_from_avg_last_month']

# Create the plot
plt.figure(figsize=(14, 7))

# Plot today's values
plt.plot(time, today, label='Today', marker='o')

# Plot the average of last week and last month
plt.plot(time, avg_last_week, label='Avg Last Week', linestyle='--')
plt.plot(time, avg_last_month, label='Avg Last Month', linestyle='--')

# Highlight anomalies
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

# Display the plot
plt.show()
import matplotlib.pyplot as plt

# Create the plot again without fill_between
plt.figure(figsize=(14, 7))

# Plot today's values
plt.plot(time, today, label='Today', marker='o')

# Plot the average of last week and last month
plt.plot(time, avg_last_week, label='Avg Last Week', linestyle='--')
plt.plot(time, avg_last_month, label='Avg Last Month', linestyle='--')

# Highlight anomalies with red and orange points
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

# Display the plot
plt.show()
