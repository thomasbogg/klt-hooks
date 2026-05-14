import os

try:
    # Check if running in deployed environment (e.g., on a server) 
    # where environment variables are set directly
    LOCAL: bool = os.getenv('LOCAL').lower() == 'true'
except Exception:
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    LOCAL: bool = os.getenv('LOCAL').lower() == 'true'


KLT_SECRET_KEY = os.getenv('KLT_SECRET_KEY')
REVOLUT_SECRET_KEY = os.getenv('REVOLUT_API_SECRET_KEY')