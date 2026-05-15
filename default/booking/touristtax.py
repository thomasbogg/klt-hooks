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
        super().__init__(database, 'touristtax', foreignKeys=['chargesId'])

    # Basic properties
    @property
    def chargesId(self) -> int | None:
        """
        Get the charges ID.
        
        Returns:
            The ID of the associated charges
        """
        return self._get('chargesId')

    @chargesId.setter
    def chargesId(self, value: int) -> None:
        """
        Set the charges ID.
        
        Args:
            value: The charges ID to set
        """
        self._set('chargesId', value)

    @property
    def total(self) -> float | None:
        """
        Get the total used for this charge.
        
        Returns:
            The total
        """
        return self._get('total')
    
    @total.setter
    def total(self, value: float) -> None:
        """
        Set the total for this charge.
        
        Args:
            value: The total to set
        """
        self._set('total', value)

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
    def orderToken(self) -> str | None:
        """
        Get order token information.
        
        Returns:
            Order token information
        """
        return self._get('orderToken')
    
    @orderToken.setter
    def orderToken(self, value: str) -> None:
        """
        Set order token information.
        
        Args:
            value: Order token information to set
        """
        self._set('orderToken', value)

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