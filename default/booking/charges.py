from default.settings import GBP_EUR_EXCHANGE_RATE
from libraries.database.row import Row as DatabaseRow
from default.booking.touristtax import Touristtax


class Charges(DatabaseRow):
    """
    Represents the financial charges associated with a booking.
    Handles currency conversion between GBP and EUR based on configuration.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Charges instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'charges', foreignKeys=['bookingId'])
        self._applyExchangeRate = True
        self._actualCurrency = None
        self._hide = False
        self._touristtax = Touristtax(database)

    def _get(self, column: str) -> object:
        """
        Get a column value with optional currency conversion.
        
        Args:
            column: The column name to retrieve
            
        Returns:
            The column value, possibly converted to EUR if applicable
        """
        value = super()._get(column)
      
        if column in self._non_money_columns():
            if value == 'GBP' and self._applyExchangeRate:
                return 'EUR'
            return value
        
        if self._hide:
            return 'Und.'
      
        if self._applyExchangeRate:
            if self._actualCurrency is None:
                self._actualCurrency = super()._get('currency')
            if self._actualCurrency == 'GBP':
                return value * GBP_EUR_EXCHANGE_RATE
      
        return value
    
    def _non_money_columns(self) -> list[str]:
        """
        Get a list of column names that don't represent monetary values.
        
        Returns:
            List of non-monetary column names
        """
        return [
            'id',
            'bookingId',
            'currency',
            'bankTransfer',
            'creditCard',
            'securityMethod',
            'manualCharges'
        ]

    # Basic properties
    @property
    def bookingId(self) -> int | None:
        """
        Get the booking ID.
        
        Returns:
            The ID of the associated booking
        """
        return self._get('bookingId')

    @bookingId.setter
    def bookingId(self, value: int) -> None:
        """
        Set the booking ID.
        
        Args:
            value: The booking ID to set
        """
        self._set('bookingId', value)

    @property
    def currency(self) -> str | None:
        """
        Get the currency used for this charge.
        
        Returns:
            The currency code (e.g., 'EUR', 'GBP')
        """
        return self._get('currency')
    
    @currency.setter
    def currency(self, value: str) -> None:
        """
        Set the currency for this charge.
        
        Args:
            value: The currency code to set (e.g., 'EUR', 'GBP')
        """
        self._set('currency', value)

    # Payment methods
    @property
    def bankTransfer(self) -> bool | str | None:
        """
        Get bank transfer information.
        
        Returns:
            Bank transfer details or status
        """
        return self._get('bankTransfer')

    @bankTransfer.setter
    def bankTransfer(self, value: bool | str) -> None:
        """
        Set bank transfer information.
        
        Args:
            value: Bank transfer details or status
        """
        self._set('bankTransfer', value)

    @property
    def creditCard(self) -> bool | str | None:
        """
        Get credit card payment information.
        
        Returns:
            Credit card details or status
        """
        return self._get('creditCard')
    
    @creditCard.setter
    def creditCard(self, value: bool | str) -> None:
        """
        Set credit card payment information.
        
        Args:
            value: Credit card details or status
        """
        self._set('creditCard', value)

    # Fee amounts
    @property
    def basicRental(self) -> float | str | None:
        """
        Get the basic rental amount.
        
        Returns:
            The basic rental amount or 'Und.' if hidden
        """
        return self._get('basicRental')
    
    @basicRental.setter
    def basicRental(self, value: float) -> None:
        """
        Set the basic rental amount.
        
        Args:
            value: The basic rental amount to set
        """
        self._set('basicRental', value)

    @property
    def admin(self) -> float | str | None:
        """
        Get the admin fee amount.
        
        Returns:
            The admin fee amount or 'Und.' if hidden
        """
        return self._get('admin')

    @admin.setter
    def admin(self, value: float) -> None:
        """
        Set the admin fee amount.
        
        Args:
            value: The admin fee amount to set
        """
        self._set('admin', value)
    
    @property
    def adminFee(self) -> float | str | None:
        """
        Alias for admin property.
        
        Returns:
            The admin fee amount or 'Und.' if hidden
        """
        return self._get('admin')

    @adminFee.setter
    def adminFee(self, value: float) -> None:
        """
        Alias setter for admin property.
        
        Args:
            value: The admin fee amount to set
        """
        self._set('admin', value)
    
    @property
    def security(self) -> float | str | None:
        """
        Get the security deposit amount.
        
        Returns:
            The security deposit amount or 'Und.' if hidden
        """
        return self._get('security')

    @security.setter
    def security(self, value: float) -> None:
        """
        Set the security deposit amount.
        
        Args:
            value: The security deposit amount to set
        """
        self._set('security', value)
    
    @property
    def securityDeposit(self) -> float | str | None:
        """
        Alias for security property.
        
        Returns:
            The security deposit amount or 'Und.' if hidden
        """
        return self._get('security')

    @securityDeposit.setter
    def securityDeposit(self, value: float) -> None:
        """
        Alias setter for security property.
        
        Args:
            value: The security deposit amount to set
        """
        self._set('security', value)

    @property
    def securityMethod(self) -> str | None:
        """
        Get the security deposit payment method.
        
        Returns:
            The method used for the security deposit
        """
        return self._get('securityMethod') 

    @securityMethod.setter
    def securityMethod(self, value: str) -> None:
        """
        Set the security deposit payment method.
        
        Args:
            value: The method used for the security deposit
        """
        self._set('securityMethod', value)

    @property
    def securityDepositMethod(self) -> str | None:
        """
        Alias for securityMethod property.
        
        Returns:
            The method used for the security deposit
        """
        return self._get('securityMethod') 

    @securityDepositMethod.setter
    def securityDepositMethod(self, value: str) -> None:
        """
        Alias setter for securityMethod property.
        
        Args:
            value: The method used for the security deposit
        """
        self._set('securityMethod', value)

    @property
    def platformFee(self) -> float | str | None:
        """
        Get the platform fee amount.
        
        Returns:
            The platform fee amount or 'Und.' if hidden
        """
        return self._get('platformFee') 

    @platformFee.setter
    def platformFee(self, value: float) -> None:
        """
        Set the platform fee amount.
        
        Args:
            value: The platform fee amount to set
        """
        self._set('platformFee', value)

    @property
    def extraNights(self) -> float | str | None:
        """
        Get the extra nights fee amount.
        
        Returns:
            The extra nights fee amount or 'Und.' if hidden
        """
        return self._get('extraNights') 

    @extraNights.setter
    def extraNights(self, value: float) -> None:
        """
        Set the extra nights fee amount.
        
        Args:
            value: The extra nights fee amount to set
        """
        self._set('extraNights', value)

    @property
    def manualCharges(self) -> str | bool | None:
        """
        Get information about manual charges.
        
        Returns:
            Manual charges information
        """
        return self._get('manualCharges')

    @manualCharges.setter
    def manualCharges(self, value: str | bool) -> None:
        """
        Set information about manual charges.
        
        Args:
            value: Manual charges information to set
        """
        self._set('manualCharges', value)
    
    # Calculated totals
    @property
    def totalRental(self) -> float | str:
        """
        Calculate the total rental amount (basic rental + admin fee).
        
        Returns:
            The total rental amount or 'Und.' if any component is undefined
        """
        value = self.basicRental + self.admin + self.extraNights
        if isinstance(value, str) and 'und' in value.lower():
            return 'Und.'
        return value
    
    @property
    def totalPlatform(self) -> float | str:
        """
        Calculate the total platform amount (total rental + platform fee).
        
        Returns:
            The total platform amount or 'Und.' if any component is undefined
        """
        value = self.totalRental + self.platformFee
        if isinstance(value, str) and 'und' in value.lower():
            return 'Und.'
        return value
    
    # Configuration properties
    @property
    def applyExchangeRate(self) -> bool:
        """
        Check if exchange rate should be applied.
        
        Returns:
            True if exchange rate should be applied, False otherwise
        """
        return self._applyExchangeRate
    
    @applyExchangeRate.setter
    def applyExchangeRate(self, value: bool) -> 'Charges':
        """
        Set whether exchange rate should be applied.
        
        Args:
            value: True to apply exchange rate, False otherwise
            
        Returns:
            Self for method chaining
        """
        self._applyExchangeRate = value
        self._actualCurrency = super()._get('currency')
        return self
    
    @property
    def exchangeCurrencies(self) -> bool:
        """
        Alias for applyExchangeRate property.
        
        Returns:
            True if exchange rate should be applied, False otherwise
        """
        return self._applyExchangeRate
    
    @exchangeCurrencies.setter
    def exchangeCurrencies(self, value: bool) -> None:
        """
        Alias setter for applyExchangeRate property.
        
        Args:
            value: True to apply exchange rate, False otherwise
        """
        self.applyExchangeRate = value
    
    @property
    def hide(self) -> bool:
        """
        Check if charge details should be hidden.
        
        Returns:
            True if charge details should be hidden, False otherwise
        """
        return self._hide
    
    @hide.setter
    def hide(self, value: bool) -> 'Charges':
        """
        Set whether charge details should be hidden.
        
        Args:
            value: True to hide charge details, False otherwise
            
        Returns:
            Self for method chaining
        """
        self._hide = value
        return self
    
    @property
    def touristtax(self) -> Touristtax:
        """
        Get the associated Touristtax instance.
        
        Returns:
            The Touristtax instance related to this charge
        """
        return self._touristtax
    
    # Data handling
    def set(self, load: dict) -> 'Charges':
        """
        Set properties from a dictionary including related entities.
        
        Args:
            load: Dictionary containing property data and related entity data.
            
        Returns:
            Self for method chaining.
        """
        if 'touristtax' in load:
            self._touristtax.set(load['touristtax'])
        return super().set(load)
    
    def insert(self) -> None:
        """
        Insert the charge and its related tourist tax into the database.
        """
        self.id = super().insert()
        self._touristtax.chargesId = self.id
        self._touristtax.insert()
    
    def update(self) -> None:
        """
        Update the charge and its related tourist tax in the database.
        """
        super().update()
        self._touristtax.chargesId = self.id
        if self._touristtax.exists():
            self._touristtax.update()
        else:
            self._touristtax.insert()

    def delete(self) -> None:
        """
        Delete the charge and its related tourist tax from the database.
        """
        self._touristtax.delete()
        super().delete()
    
    def __str__(self) -> str:
        """
        String representation of the Charges instance including tourist tax details.
        
        Returns:
            A string representation of the Charges instance
        """
        string = super().__str__()
        string += self._touristtax.__str__()
        return string