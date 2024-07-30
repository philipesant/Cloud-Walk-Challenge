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
-- Example of inserting data into transactions_1
INSERT INTO transactions_1 (timestamp, status, amount) VALUES ('2024-07-30 10:00:00', 'approved', 100.0);
INSERT INTO transactions_1 (timestamp, status, amount) VALUES ('2024-07-30 10:01:00', 'failed', 50.0);
-- Continue inserting the rest of the data...

-- Example of inserting data into transactions_2
INSERT INTO transactions_2 (timestamp, status, amount) VALUES ('2024-07-30 10:03:00', 'approved', 200.0);
INSERT INTO transactions_2 (timestamp, status, amount) VALUES ('2024-07-30 10:04:00', 'reversed', 100.0);
-- Continue inserting the rest of the data...
-- Create a table for alerts
CREATE TABLE alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_time TEXT,
    alert_message TEXT
);
import pandas as pd
import sqlite3

# Load the transaction data from CSV files
transactions_1 = pd.read_csv('/mnt/data/transactions_1.csv')
transactions_2 = pd.read_csv('/mnt/data/transactions_2.csv')

# Connect to the SQLite database
connection = sqlite3.connect('transactions.db')
cursor = connection.cursor()

# Insert data into transactions_1 table
for _, row in transactions_1.iterrows():
    cursor.execute("INSERT INTO transactions_1 (timestamp, status, amount) VALUES (?, ?, ?)",
                   (row['timestamp'], row['status'], row['amount']))

# Insert data into transactions_2 table
for _, row in transactions_2.iterrows():
    cursor.execute("INSERT INTO transactions_2 (timestamp, status, amount) VALUES (?, ?, ?)",
                   (row['timestamp'], row['status'], row['amount']))

connection.commit()
from flask import Flask, request, jsonify
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3

app = Flask(__name__)

def determine_status(row):
    if row['status'] in ['failed', 'reversed']:
        return 'problem'
    elif row['status'] == 'denied':
        return 'risk_denied'
    else:
        return 'approved'

def send_alert_email(subject, body):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "youremail@gmail.com"
    password = "yourpassword"
    receiver_email = "teamemail@example.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def monitor_alerts(cursor):
    cursor.execute("SELECT timestamp, status FROM transactions_1 WHERE timestamp > datetime('now', '-1 minute')")
    transactions = cursor.fetchall()
    problem_count = sum(1 for t in transactions if t[1] == 'problem')
    risk_denied_count = sum(1 for t in transactions if t[1] == 'risk_denied')

    threshold = 5  # Set your threshold here
    if problem_count > threshold:
        alert_message = f"High number of problem transactions detected in the last minute: {problem_count}"
        send_alert_email("Problem Transactions Alert", alert_message)
        cursor.execute("INSERT INTO alerts (alert_time, alert_message) VALUES (?, ?)", (datetime.now(), alert_message))
        connection.commit()

    if risk_denied_count > threshold:
        alert_message = f"High number of risk denied transactions detected in the last minute: {risk_denied_count}"
        send_alert_email("Risk Denied Transactions Alert", alert_message)
        cursor.execute("INSERT INTO alerts (alert_time, alert_message) VALUES (?, ?)", (datetime.now(), alert_message))
        connection.commit()

@app.route('/transaction', methods=['POST'])
def transaction():
    data = request.json
    timestamp = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
    status = determine_status(data)
    amount = data['amount']

    cursor.execute("INSERT INTO transactions_1 (timestamp, status, amount) VALUES (?, ?, ?)", (timestamp, status, amount))
    connection.commit()

    monitor_alerts(cursor)

    return jsonify({'message': 'Transaction processed'}), 200

if __name__ == '__main__':
    connection = sqlite3.connect('transactions.db', check_same_thread=False)
    cursor = connection.cursor()
    app.run(debug=True)
import time

def continuous_monitoring():
    while True:
        monitor_alerts(cursor)
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    continuous_monitoring()
import matplotlib.pyplot as plt

def visualize_transactions():
    cursor.execute("SELECT timestamp, status, COUNT(*) FROM transactions_1 GROUP BY timestamp, status")
    data = cursor.fetchall()

    timestamps = [row[0] for row in data]
    counts = [row[2] for row in data]

    plt.figure(figsize=(14, 7))
    plt.plot(timestamps, counts, marker='o', linestyle='-')
    plt.xlabel('Timestamp')
    plt.ylabel('Number of Transactions')
    plt.title('Real-time Transactions Monitoring')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.show()

# Call this function periodically to update the chart
visualize_transactions()
