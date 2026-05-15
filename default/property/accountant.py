from typing import Any

from libraries.database.row import Row as DatabaseRow


class Accountant(DatabaseRow):
    """
    Represents a property accountant with company, contact, and communication details.
    
    This class handles database operations for property accountants, allowing
    retrieval and modification of accountant information including company name,
    contact name, email, and phone number.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property accountant object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertyAccountants')

    @property
    def company(self) -> str | None:
        """
        Get the accountant's company name.
        
        Returns:
            The company name or None if not set.
        """
        return self._get('company')
    
    @company.setter
    def company(self, value: str) -> None:
        """
        Set the accountant's company name.
        
        Args:
            value: The company name to set.
        """
        self._set('company', value)

    @property
    def name(self) -> str | None:
        """
        Get the accountant's contact name.
        
        Returns:
            The contact name or None if not set.
        """
        return self._get('name')

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the accountant's contact name.
        
        Args:
            value: The contact name to set.
        """
        self._set('name', value)

    @property
    def email(self) -> str | None:
        """
        Get the accountant's email address.
        
        Returns:
            The email address or None if not set.
        """
        return self._get('email')

    @email.setter
    def email(self, value: str) -> None:
        """
        Set the accountant's email address.
        
        Args:
            value: The email address to set.
        """
        self._set('email', value)

    @property
    def phone(self) -> str | None:
        """
        Get the accountant's phone number.
        
        Returns:
            The phone number or None if not set.
        """
        return self._get('phone')

    @phone.setter
    def phone(self, value: str) -> None:
        """
        Set the accountant's phone number.
        
        Args:
            value: The phone number to set.
        """
        self._set('phone', value)
    
    def _get_condition(self) -> str:
        """
        Get the database condition to identify this accountant record.
        
        Returns:
            A SQL condition string based on the company name.
        """
        return f'company="{self.company}"'