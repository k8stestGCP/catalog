from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

supabase_url = os.getenv("URL")
supabase_key = os.getenv("KEY")

supabase: Client = create_client(supabase_url, supabase_key)

def verify_user(token: str):
    response = supabase.auth.api.get_user(token)
    return response.user if response.user else None
