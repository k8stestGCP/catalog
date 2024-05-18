# test_db_connection.py

from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from urllib.parse import quote
# Load environment variables from .env file
load_dotenv()

username = "postgres.kbeerramjqhmtihclfzm"
password = "XibaXilena@10"
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"

# Encode password
encoded_password = quote(password)

# Construct the DATABASE_URL
username = "postgres.tuwcjjvparuzuuttkxva"
password = "nmnO0SmlF7pSswJW"
host = "aws-0-us-east-1.pooler.supabase.com"
port = 5432
database = "postgres"

# Encode password
encoded_password = quote(password)

# Construct the DATABASE_URL
DATABASE_URL = f"postgresql://{username}:{encoded_password}@{host}:{port}/{database}"
print(DATABASE_URL)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment variables")

# Create engine
engine = create_engine(DATABASE_URL)

# Test connection
try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Error connecting to database: {e}")
