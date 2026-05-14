import os

from default.google.accounts import KLTGoogleAccount

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

# REVOLUT credentials
REVOLUT_SECRET_KEY = os.getenv('REVOLUT_API_SECRET_KEY')
REVOLUT_API_VERSION = os.getenv('REVOLUT_API_VERSION')


#######################################################
# GOOGLE CREDENTIALS & ACCOUNTS
#######################################################

if LOCAL:  
    GOOGLE_API_CREDENTIALS = os.path.abspath(os.getenv('GOOGLE_CREDS_DIR', None))
else:
    GOOGLE_API_CREDENTIALS = (
        {
            "type": os.getenv("type"),
            "project_id": os.getenv("project_id"),
            "private_key_id": os.getenv("private_key_id"),
            "private_key": '\n'.join(os.getenv("private_key").split('\\n')),
            "client_email": os.getenv("client_email"),
            "client_id": os.getenv("client_id"),
            "auth_uri": os.getenv("auth_uri"),
            "token_uri": os.getenv("token_uri"),
            "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
            "client_x509_cert_url": os.getenv("client_x509_cert_url"),
            "universe_domain": os.getenv("universe_domain"),
        },
        os.getenv('GOOGLE_API_SERVICE_ACCOUNT_USERNAME'),
    )

TeamAtABA = KLTGoogleAccount(details=os.getenv('TEAM_@_ABA').split(';'), credentials=GOOGLE_API_CREDENTIALS, local=LOCAL)
ThomasAtABA = KLTGoogleAccount(details=os.getenv('THOMAS_@_ABA').split(';'), credentials=GOOGLE_API_CREDENTIALS, local=LOCAL)
KevinAtABA = KLTGoogleAccount(details=os.getenv('KEVIN_@_ABA').split(';'), credentials=GOOGLE_API_CREDENTIALS, local=LOCAL)

# Default account for Google API operations
DEFAULT_ACCOUNT = KLTGoogleAccount(details=os.getenv('DEFAULT_ACCOUNT').split(';'), credentials=GOOGLE_API_CREDENTIALS, local=LOCAL)