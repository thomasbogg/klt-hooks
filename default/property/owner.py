from typing import Any

from libraries.database.row import Row as DatabaseRow


class Owner(DatabaseRow):
    """
    Represents a property owner with contact details and preferences.
    
    This class handles database operations for property owners, allowing
    retrieval and modification of contact information, cleaning preferences,
    payment preferences, and accounting settings.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property owner object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertyOwners')

    # Basic owner information
    @property
    def name(self) -> str | None:
        """
        Get the owner's name.
        
        Returns:
            The owner's name or None if not set.
        """
        return self._get('name')

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the owner's name.
        
        Args:
            value: The name to set.
        """
        self._set('name', value)

    @property
    def email(self) -> str | None:
        """
        Get the owner's email address.
        
        Returns:
            The email address or None if not set.
        """
        return self._get('email')
    
    @email.setter
    def email(self, value: str) -> None:
        """
        Set the owner's email address.
        
        Args:
            value: The email address to set.
        """
        self._set('email', value)

    @property    
    def phone(self) -> str | None:
        """
        Get the owner's phone number.
        
        Returns:
            The phone number or None if not set.
        """
        return self._get('phone')

    @phone.setter
    def phone(self, value: str) -> None:
        """
        Set the owner's phone number.
        
        Args:
            value: The phone number to set.
        """
        self._set('phone', value)

    @property    
    def nifNumber(self) -> str | None:
        """
        Get the owner's NIF (tax) number.
        
        Returns:
            The NIF number or None if not set.
        """
        return self._get('nifNumber')

    @nifNumber.setter
    def nifNumber(self, value: str) -> None:
        """
        Set the owner's NIF (tax) number.
        
        Args:
            value: The NIF number to set.
        """
        self._set('nifNumber', value)

    # Owner preferences
    @property    
    def defaultClean(self) -> bool | None:
        """
        Get whether the property has default cleaning service enabled.
        
        Returns:
            Boolean indicating if default cleaning is enabled, or None if not set.
        """
        return self._get('defaultClean')

    @defaultClean.setter
    def defaultClean(self, value: bool) -> None:
        """
        Set whether the property has default cleaning service enabled.
        
        Args:
            value: Boolean indicating if default cleaning should be enabled.
        """
        self._set('defaultClean', value)

    @property    
    def defaultMeetGreet(self) -> bool | None:
        """
        Get whether the property has default meet and greet service enabled.
        
        Returns:
            Boolean indicating if meet and greet is enabled, or None if not set.
        """
        return self._get('defaultMeetGreet')

    @defaultMeetGreet.setter
    def defaultMeetGreet(self, value: bool) -> None:
        """
        Set whether the property has default meet and greet service enabled.
        
        Args:
            value: Boolean indicating if meet and greet should be enabled.
        """
        self._set('defaultMeetGreet', value)

    # Payment preferences
    @property    
    def takesEuros(self) -> bool | None:
        """
        Get whether the owner accepts payments in Euros.
        
        Returns:
            Boolean indicating if Euro payments are accepted, or None if not set.
        """
        return self._get('takesEuros')

    @takesEuros.setter
    def takesEuros(self, value: bool) -> None:
        """
        Set whether the owner accepts payments in Euros.
        
        Args:
            value: Boolean indicating if Euro payments should be accepted.
        """
        self._set('takesEuros', value)

    @property    
    def takesPounds(self) -> bool | None:
        """
        Get whether the owner accepts payments in British Pounds.
        
        Returns:
            Boolean indicating if Pound payments are accepted, or None if not set.
        """
        return self._get('takesPounds')

    @takesPounds.setter
    def takesPounds(self, value: bool) -> None:
        """
        Set whether the owner accepts payments in British Pounds.
        
        Args:
            value: Boolean indicating if Pound payments should be accepted.
        """
        self._set('takesPounds', value)

    @property
    def takesBothCurrencies(self) -> bool:
        """
        Get whether the owner accepts payments in both Euros and British Pounds.
        
        Returns:
            Boolean indicating if both currencies are accepted.
        """
        return bool(self.takesEuros and self.takesPounds)

    # Accounting settings
    @property    
    def wantsAccounting(self) -> bool | None:
        """
        Get whether the owner wants accounting services.
        
        Returns:
            Boolean indicating if accounting services are requested, or None if not set.
        """
        return self._get('wantsAccounting')

    @wantsAccounting.setter
    def wantsAccounting(self, value: bool) -> None:
        """
        Set whether the owner wants accounting services.
        
        Args:
            value: Boolean indicating if accounting services are requested.
        """
        self._set('wantsAccounting', value)

    @property    
    def cleansAreInvoiced(self) -> bool | None:
        """
        Get whether cleaning services are invoiced to the owner.
        
        Returns:
            Boolean indicating if cleanings are invoiced, or None if not set.
        """
        return self._get('cleansAreInvoiced')

    @cleansAreInvoiced.setter
    def cleansAreInvoiced(self, value: bool) -> None:
        """
        Set whether cleaning services are invoiced to the owner.
        
        Args:
            value: Boolean indicating if cleanings should be invoiced.
        """
        self._set('cleansAreInvoiced', value)

    @property    
    def rentalCommissionsAreInvoiced(self) -> bool | None:
        """
        Get whether rental commissions are invoiced to the owner.
        
        Returns:
            Boolean indicating if commissions are invoiced, or None if not set.
        """
        return self._get('rentalCommissionsAreInvoiced')

    @rentalCommissionsAreInvoiced.setter
    def rentalCommissionsAreInvoiced(self, value: bool) -> None:
        """
        Set whether rental commissions are invoiced to the owner.
        
        Args:
            value: Boolean indicating if commissions should be invoiced.
        """
        self._set('rentalCommissionsAreInvoiced', value)

    @property    
    def isPaidRegularly(self) -> bool | None:
        """
        Get whether the owner is paid on a regular schedule.
        
        Returns:
            Boolean indicating if the owner is paid regularly, or None if not set.
        """
        return self._get('isPaidRegularly')

    @isPaidRegularly.setter
    def isPaidRegularly(self, value: bool) -> None:
        """
        Set whether the owner is paid on a regular schedule.
        
        Args:
            value: Boolean indicating if the owner should be paid regularly.
        """
        self._set('isPaidRegularly', value)

    def _get_condition(self) -> str:
        """
        Get the database condition to identify this owner record.
        
        Returns:
            A SQL condition string based on the owner's name.
        """
        _condition = f'name="{self.name}"'
        try:
            _condition += f' OR email="{self.email}"'
        except KeyError:
            pass
        return _condition