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

-- Calculate descriptive statistics for checkout_data_2
SELECT
    AVG(today) AS avg_today,
    STDDEV(today) AS stddev_today,
    AVG(yesterday) AS avg_yesterday,
    AVG(same_day_last_week) AS avg_same_day_last_week,
    AVG(avg_last_week) AS avg_avg_last_week,
    AVG(avg_last_month) AS avg_avg_last_month
FROM
    checkout_data_2;
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

-- Calculate deviations and anomalies for checkout_data_2
SELECT
    time,
    today,
    today - yesterday AS deviation_yesterday,
    today - same_day_last_week AS deviation_same_day_last_week,
    today - avg_last_week AS deviation_avg_last_week,
    today - avg_last_month AS deviation_avg_last_month,
    CASE WHEN ABS(today - yesterday) > 2 * (SELECT STDDEV(today - yesterday) FROM checkout_data_2) THEN 1 ELSE 0 END AS anomaly_yesterday,
    CASE WHEN ABS(today - same_day_last_week) > 2 * (SELECT STDDEV(today - same_day_last_week) FROM checkout_data_2) THEN 1 ELSE 0 END AS anomaly_same_day_last_week,
    CASE WHEN ABS(today - avg_last_week) > 2 * (SELECT STDDEV(today - avg_last_week) FROM checkout_data_2) THEN 1 ELSE 0 END AS anomaly_avg_last_week,
    CASE WHEN ABS(today - avg_last_month) > 2 * (SELECT STDDEV(today - avg_last_month) FROM checkout_data_2) THEN 1 ELSE 0 END AS anomaly_avg_last_month
FROM
    checkout_data_2;
