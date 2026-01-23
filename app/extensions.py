import os
from supabase import create_client, Client

# Global client variable
supabase: Client = None

def init_supabase():
    """Initialize the Supabase client using env vars."""
    global supabase
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        # In testing, we might not have keys, so we skip or mock
        return

    supabase = create_client(url, key)