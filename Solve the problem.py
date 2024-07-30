import pandas as pd

# Load the transaction data from CSV files
transactions_1 = pd.read_csv('transactions_1.csv')
transactions_2 = pd.read_csv('transactions_1.csv')

# Display the first few rows of each dataset
transactions_1.head(), transactions_2.head()
import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('transactions.db')
cursor = connection.cursor()

# Create tables if they don't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    status TEXT,
    amount REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alert_time TEXT,
    alert_message TEXT
)
''')

connection.commit()
from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def monitor_alerts():
    cursor.execute("SELECT timestamp, status FROM transactions WHERE timestamp > datetime('now', '-1 minute')")
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

    cursor.execute("INSERT INTO transactions (timestamp, status, amount) VALUES (?, ?, ?)", (timestamp, status, amount))
    connection.commit()

    monitor_alerts()

    return jsonify({'message': 'Transaction processed'}), 200

if __name__ == '__main__':
    app.run(debug=True)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import sqlite3
import time

# Connect to the database
connection = sqlite3.connect('transactions.db')
cursor = connection.cursor()

# Email server configuration
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "youremail@gmail.com"
password = "yourpassword"
receiver_email = "teamemail@example.com"

def send_alert_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        print(f"Error: {e}")

def monitor_alerts():
    # Check transactions in the last minute
    cursor.execute("SELECT timestamp, status FROM transactions WHERE timestamp > datetime('now', '-1 minute')")
    transactions = cursor.fetchall()

    # Count problem and risk denied transactions
    problem_count = sum(1 for t in transactions if t[1] == 'problem')
    risk_denied_count = sum(1 for t in transactions if t[1] == 'risk_denied')

    # Set thresholds for alerts
    problem_threshold = 5
    risk_denied_threshold = 5

    # Send alerts for problem transactions
    if problem_count > problem_threshold:
        alert_message = f"High number of problem transactions detected in the last minute: {problem_count}"
        send_alert_email("Problem Transactions Alert", alert_message)
        cursor.execute("INSERT INTO alerts (alert_time, alert_message) VALUES (?, ?)", (datetime.now(), alert_message))
        connection.commit()

    # Send alerts for risk denied transactions
    if risk_denied_count > risk_denied_threshold:
        alert_message = f"High number of risk denied transactions detected in the last minute: {risk_denied_count}"
        send_alert_email("Risk Denied Transactions Alert", alert_message)
        cursor.execute("INSERT INTO alerts (alert_time, alert_message) VALUES (?, ?)", (datetime.now(), alert_message))
        connection.commit()

# Function to continuously monitor transactions
def continuous_monitoring():
    while True:
        monitor_alerts()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    continuous_monitoring()
import matplotlib.pyplot as plt

def visualize_transactions():
    cursor.execute("SELECT timestamp, status, COUNT(*) FROM transactions GROUP BY timestamp, status")
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
