import sqlite3
import pandas as pd

# Path to the CSV files
csv_files = {
    'transactions_1': 'path/to/transactions_1.csv',
    'transactions_2': 'path/to/transactions_2.csv'
}

# Create an in-memory SQLite database
connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

# Create tables with the correct schema
create_transactions_1_table = '''
    CREATE TABLE transactions_1 (
        time TEXT,
        status TEXT,
        f0_ INTEGER
    );
'''

create_transactions_2_table = '''
    CREATE TABLE transactions_2 (
        time TEXT,
        status TEXT,
        count INTEGER
    );
'''

# Execute the table creation queries
cursor.execute("DROP TABLE IF EXISTS transactions_1;")
cursor.execute(create_transactions_1_table)

cursor.execute("DROP TABLE IF EXISTS transactions_2;")
cursor.execute(create_transactions_2_table)

# Load CSV data into DataFrames
transactions_1_df = pd.read_csv(csv_files['transactions_1'])
transactions_2_df = pd.read_csv(csv_files['transactions_2'])

# Insert data into the tables
transactions_1_df.to_sql('transactions_1', connection, if_exists='append', index=False)
transactions_2_df.to_sql('transactions_2', connection, if_exists='append', index=False)

# Verify the contents of the tables
result_df_1 = pd.read_sql_query("SELECT * FROM transactions_1 LIMIT 5;", connection)
result_df_2 = pd.read_sql_query("SELECT * FROM transactions_2 LIMIT 5;", connection)

# Display results
print("Transactions 1 Table Sample:")
print(result_df_1)

print("\nTransactions 2 Table Sample:")
print(result_df_2)

# Close the connection
connection.close()
