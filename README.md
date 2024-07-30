# Cloud Walk Challenge

This repository contains solutions to the Cloud Walk Challenge. The challenge involves analyzing checkout and transaction data to derive meaningful insights using SQL queries and Python scripting.

## Project Structure

The project is organized as follows:


### Files and Directories

- **Python Scripts:**
  - `Get your hands dirty step 1.py`: Contains SQL queries for creating tables and inserting checkout data.
  - `Get You hands dirty Step 2.py`: Contains SQL queries similar to step 1 for further analysis or modifications.
  - `Solve the problem.py`: Contains SQL queries for creating transaction tables and inserting transaction data.

- **Data Files (CSV):**
  - `checkout_data_1.csv`: Contains checkout data with metrics for today, yesterday, and previous weeks/months.
  - `checkout_data_2.csv`: Another set of checkout data with similar metrics.
  - `transactions_1.csv`: Transaction data with time, status, and count metrics.
  - `transactions_2.csv`: Another set of transaction data with time, status, and count metrics.

## Setup Instructions

To run the SQL scripts and analyze the data, follow these steps:

### Requirements

Ensure you have the following installed:

- Python 3.x
- SQLite

### Instructions

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd Cloud-Walk-Challenge-main
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
    time TEXT,
    status TEXT,
    f0_ INTEGER
);

CREATE TABLE transactions_2 (
    time TEXT,
    status TEXT,
    count INTEGER
);
python "Get your hands dirty step 1.py"
python "Get You hands dirty Step 2.py"
python "Solve the problem.py"
