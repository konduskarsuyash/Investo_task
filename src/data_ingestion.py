import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    print("Connection successful!")
except Error as err:
    print(f"Error: {err}")

    
cursor = conn.cursor()

# Step 2: Load the dataset
data = pd.read_excel("../data/stock_data.xlsx")

# Step 3: Validate and Prepare Data
for index, row in data.iterrows():
    if not isinstance(row['close'], float) or not isinstance(row['volume'], int):
        raise ValueError(f"Invalid data at row {index}: {row}")
    # Insert into MySQL
    query = """
    INSERT INTO stock_data (datetime, close, high, low, open, volume, instrument)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        row['datetime'], row['close'], row['high'], row['low'], row['open'], row['volume'], row['instrument']
    )
    cursor.execute(query, values)

# Commit changes
conn.commit()
cursor.close()
conn.close()
