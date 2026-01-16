import pandas as pd
from pymongo import MongoClient
import logging
import os
from dotenv import load_dotenv
import time

# ------------------- LOGGING -------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------- MONGODB CONFIG -------------------
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME")
RAW_DATA_COLLECTION = os.getenv("MONGO_COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
raw_col = db[RAW_DATA_COLLECTION]

# ------------------- LOAD CSV DATA -------------------
def load_csv_to_mongodb():
    """
    Load groundwater CSV data into MongoDB
    """
    try:
        # Load groundwater.csv
        df = pd.read_csv("groundwater.csv")
        logging.info(f"Loaded groundwater.csv with {len(df)} records")
        
        # Rename columns to match schema
        df.rename(columns={
            'State': 'state',
            'Date': 'date',
            'Water_Level_m_bgl': 'water_level'
        }, inplace=True)
        
        # Remove Time column (not needed)
        df = df.drop('Time', axis=1)
        
        # Convert date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Drop rows with missing critical values
        df = df.dropna(subset=['state', 'water_level', 'date'])
        
        logging.info(f"After cleaning: {len(df)} records remaining")
        
        # Clear existing data
        raw_col.delete_many({})
        
        # Insert into MongoDB
        if len(df) > 0:
            records = df.to_dict('records')
            total_records = len(records)
            batch_size = 5000  # Smaller batches to avoid timeout
            
            logging.info(f"Starting insertion of {total_records} records into MongoDB in batches of {batch_size}...")
            
            # Insert in batches to show progress
            for i in range(0, total_records, batch_size):
                try:
                    batch = records[i:i+batch_size]
                    raw_col.insert_many(batch)
                    progress = min(i + batch_size, total_records)
                    percentage = (progress / total_records) * 100
                    logging.info(f"Progress: {progress}/{total_records} records inserted ({percentage:.1f}%)")
                    time.sleep(0.5)  # Small delay between batches
                except Exception as batch_error:
                    logging.warning(f"Batch insertion failed at record {i}, retrying...")
                    time.sleep(2)
                    try:
                        raw_col.insert_many(batch)
                        progress = min(i + batch_size, total_records)
                        percentage = (progress / total_records) * 100
                        logging.info(f"Progress: {progress}/{total_records} records inserted ({percentage:.1f}%)")
                    except Exception as retry_error:
                        logging.error(f"Failed to insert batch at {i}: {str(retry_error)}")
                        raise
            
            logging.info(f"✓ Successfully inserted all {total_records} records into MongoDB")
        else:
            logging.warning("No valid records to insert")
            
    except Exception as e:
        logging.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    load_csv_to_mongodb()
