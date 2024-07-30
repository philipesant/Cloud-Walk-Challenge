-- Load the CSV files into a SQL table
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

-- Insert data into the tables (for illustration; use appropriate method for bulk insert)
-- Example for inserting data into checkout_data_1
INSERT INTO checkout_data_1 VALUES ('00h', 9, 12, 11, 6.42, 4.85);
INSERT INTO checkout_data_1 VALUES ('01h', 3, 5, 1, 1.85, 1.92);
-- Continue inserting the rest of the data...

-- Calculate descriptive statistics for checkout_data_1
SELECT
    AVG(today) AS avg_today,
    STDDEV(today) AS stddev_today,
    AVG(yesterday) AS avg_yesterday,
    AVG(same_day_last_week) AS avg_same_day_last_week,
    AVG(avg_last_week) AS avg_avg_last_week,
    AVG(avg_last_month) AS avg_avg_last_month
FROM
    checkout_data_1;

-- Calculate deviations and anomalies for checkout_data_1
SELECT
    time,
    today,
    today - yesterday AS deviation_yesterday,
    today - same_day_last_week AS deviation_same_day_last_week,
    today - avg_last_week AS deviation_avg_last_week,
    today - avg_last_month AS deviation_avg_last_month,
    CASE WHEN ABS(today - yesterday) > 2 * (SELECT STDDEV(today - yesterday) FROM checkout_data_1) THEN 1 ELSE 0 END AS anomaly_yesterday,
    CASE WHEN ABS(today - same_day_last_week) > 2 * (SELECT STDDEV(today - same_day_last_week) FROM checkout_data_1) THEN 1 ELSE 0 END AS anomaly_same_day_last_week,
    CASE WHEN ABS(today - avg_last_week) > 2 * (SELECT STDDEV(today - avg_last_week) FROM checkout_data_1) THEN 1 ELSE 0 END AS anomaly_avg_last_week,
    CASE WHEN ABS(today - avg_last_month) > 2 * (SELECT STDDEV(today - avg_last_month) FROM checkout_data_1) THEN 1 ELSE 0 END AS anomaly_avg_last_month
FROM
    checkout_data_1;

-- Repeat similar calculations for checkout_data_2
