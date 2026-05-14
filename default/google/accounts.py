from libraries.google.account import GoogleAccount

class KLTGoogleAccount(GoogleAccount):
    """
    Google Account for KLT users at Algarve Beach Apartments.
    
    This class represents a Google account with contact information
    and credentials for API access.
    """
    def __init__(self, details: list[str], credentials: str | tuple, local: bool = False) -> None:
        """
        Initialize the KLT Google Account.
        
        Args:
            details: List containing the account details.
            credentials: Directory path where API credentials are stored.
            local: Flag indicating if the account is for local development.
        """
        super().__init__()
        self.name: str = details[0]
        self.emailAddress: str = details[1]
        self.phoneNumber: str = details[2]
        self.details: list[str] = details[3:]
        self.credentials: str = credentials
        self.local: bool = local