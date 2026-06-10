from libraries.database.row import Row as DatabaseRow


class Touristtax(DatabaseRow):
    """
    Represents the financial charges associated with a booking.
    Handles currency conversion between GBP and EUR based on configuration.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Touristtax instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'touristtax')

    # Basic properties
    @property
    def date(self) -> str | None:
        """
        Get the date information.
        
        Returns:
            The date information
        """
        return self._get('date')

    @date.setter
    def date(self, value: str) -> None:
        """
        Set the date information.
        
        Args:
            value: The date information to set
        """
        self._set('date', value)

    @property
    def orderId(self) -> str | None:
        """
        Get order ID information.
        
        Returns:
            Order ID information
        """
        return self._get('orderId')

    @orderId.setter
    def orderId(self, value: str) -> None:
        """
        Set order ID information.
        
        Args:
            value: Order ID information to set
        """
        self._set('orderId', value)

    @property
    def paid(self) -> bool | None:
        """
        Get the payment status.
        
        Returns:
            The payment status«
        """
        return self._get('paid')
    
    @paid.setter
    def paid(self, value: bool) -> None:
        """
        Set the payment status.
        
        Args:
            value: The payment status to set
        """
        self._set('paid', value)