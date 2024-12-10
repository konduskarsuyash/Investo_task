import pandas as pd
import unittest
import mysql.connector
from datetime import datetime

class TestDataValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load dataset
        cls.data = pd.read_excel("../data/stock_data.xlsx")
    
    def test_columns_present(self):
        """Test if all required columns are present"""
        required_columns = {'datetime', 'close', 'high', 'low', 'open', 'volume', 'instrument'}
        self.assertTrue(required_columns.issubset(self.data.columns), "Missing required columns!")

    def test_no_missing_values(self):
        """Test if there are no missing values in the dataset"""
        self.assertFalse(self.data.isnull().any().any(), "Dataset contains missing values!")
    
    def test_column_types(self):
        """Test if column types are valid"""
        for index, row in self.data.iterrows():
            self.assertIsInstance(row['datetime'], pd.Timestamp, f"Invalid datetime at row {index}")
            self.assertIsInstance(row['close'], float, f"Invalid close value at row {index}")
            self.assertIsInstance(row['high'], float, f"Invalid high value at row {index}")
            self.assertIsInstance(row['low'], float, f"Invalid low value at row {index}")
            self.assertIsInstance(row['open'], float, f"Invalid open value at row {index}")
            self.assertIsInstance(row['volume'], int, f"Invalid volume value at row {index}")
            self.assertIsInstance(row['instrument'], str, f"Invalid instrument value at row {index}")
    
    def test_no_duplicate_rows(self):
        """Test if there are no duplicate rows"""
        self.assertTrue(self.data.duplicated().sum() == 0, "Dataset contains duplicate rows!")
    
    def test_datetime_range(self):
        """Test if datetime values are within a reasonable range"""
        for index, date in enumerate(self.data['datetime']):
            self.assertTrue(date <= datetime.now(), f"Future date found at row {index}: {date}")
    
    def test_valid_instrument(self):
        """Test if instrument column contains valid ticker symbols"""
        for index, instrument in enumerate(self.data['instrument']):
            self.assertTrue(len(instrument) > 0, f"Invalid instrument at row {index}")
    
    def test_database_insert(self):
        """Test if data can be inserted into the database"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="suyash@123",
                database="investo_internship"
            )
            cursor = conn.cursor()
            
            # Clear table before testing
            cursor.execute("DELETE FROM stock_data")
            conn.commit()
            
            # Insert test data
            for index, row in self.data.iterrows():
                query = """
                INSERT INTO stock_data (datetime, close, high, low, open, volume, instrument)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    row['datetime'], row['close'], row['high'], row['low'],
                    row['open'], row['volume'], row['instrument']
                )
                cursor.execute(query, values)
            conn.commit()

            # Check row count
            cursor.execute("SELECT COUNT(*) FROM stock_data")
            row_count = cursor.fetchone()[0]
            self.assertEqual(row_count, len(self.data), "Row count mismatch in database!")

        finally:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    unittest.main()
