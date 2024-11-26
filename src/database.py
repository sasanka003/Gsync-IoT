from supabase import create_client
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def insert_data_to_supabase(data):
    """Insert sensor data into Supabase database."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase URL or API key is missing in the environment variables.")
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = supabase.table("sensor_data").insert(data).execute()
    if response.status_code == 200:
        print("Data successfully inserted into Supabase!")
    else:
        print(f"Failed to insert data: {response.json()}")