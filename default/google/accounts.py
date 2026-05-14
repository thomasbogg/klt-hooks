from libraries.google.account import GoogleAccount
import os

try:
    # Check if running in deployed environment (e.g., on a server) 
    # where environment variables are set directly
    LOCAL: bool = os.getenv('LOCAL').lower() == 'true'
except Exception:
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    LOCAL = os.getenv('LOCAL').lower() == 'true'


if LOCAL:  
    CREDS = os.path.abspath(os.getenv('GOOGLE_CREDS_DIR', None))
else:
    CREDS = (
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
        #os.getenv('GOOGLE_API_CREDENTIALS_DIR'),
        os.getenv('GOOGLE_API_SERVICE_ACCOUNT_USERNAME'),
    )


class ThomasAtABA(GoogleAccount):
    """
    Google Account for Thomas at Algarve Beach Apartments.
    
    This class represents Thomas Bogg's Google account with contact information
    and credentials for API access.
    """

    _details: list = os.getenv('ThomasAtABA').split(';')

    
    def __init__(self, credentials: str = CREDS, local: bool = LOCAL) -> None:
        """
        Initialize the Thomas Bogg Google Account.
        
        Args:
            credentials: Directory path where API credentials are stored.
        """
        super().__init__()
        self.name: str = self._details[0]
        self.emailAddress: str = self._details[1]
        self.phoneNumber: str = self._details[2]
        self.details: list[str] = self._details[3:]
        self.credentials: str = credentials
        self.local: bool = local


class KevinAtABA(GoogleAccount):
    """
    Google Account for Kevin at Algarve Beach Apartments.
    
    This class represents Kevin Bogg's Google account with contact information
    and credentials for API access.
    """

    _details: list = os.getenv('KevinAtABA').split(';')
    
    def __init__(self, credentials: str = CREDS, local: bool = LOCAL) -> None:
        """
        Initialize the Kevin Bogg Google Account.
        
        Args:
            credentials: Directory path where API credentials are stored.
        """
        super().__init__()
        self.name: str = self._details[0]
        self.emailAddress: str = self._details[1]
        self.phoneNumber: str = self._details[2]
        self.details: list[str] = self._details[3:]
        self.credentials: str = credentials
        self.local: bool = local


class TeamAtABA(GoogleAccount):
    """
    Google Account for the Management Team at Algarve Beach Apartments.
    
    This class represents the shared account for the management team with contact
    information and credentials for API access.
    """

    _details: list = os.getenv('TeamAtABA').split(';')
    
    def __init__(self, credentials: str = CREDS, local: bool = LOCAL) -> None:
        """
        Initialize the Management Team Google Account.
        
        Args:
            credentials: Directory path where API credentials are stored.
        """
        super().__init__()
        self.name: str = self._details[0]
        self.emailAddress: str = self._details[1]
        self.phoneNumber: str = self._details[2]
        self.details: list[str] = self._details[3:]
        self.credentials: str = credentials
        self.local: bool = local