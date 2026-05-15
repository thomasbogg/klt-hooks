from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Accountants(Table):
    """
    Represents the property accountants table in the database.
    
    This class provides methods to access and define columns in the propertyAccountants table.
    """

    def __init__(self) -> None:
        """
        Initialize the Accountants table.
        """
        super().__init__(name='propertyAccountants')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def company(self) -> Column | Self:
        """
        Define the company column of the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        return self._column(name='company', dataType='text')

    def name(self) -> Column | Self:
        """
        Define the name column of the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        return self._column(name='name', dataType='text')

    def email(self) -> Column | Self:
        """
        Define the email column of the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        return self._column(name='email', dataType='text')

    def phone(self) -> Column | Self:
        """
        Define the phone column of the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        return self._column(name='phone', dataType='text')
    
    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Accountants: The current instance for method chaining.
        """
        self.id()
        self.company()
        self.name()
        self.email()
        self.phone()
        return self