from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Guests(Table):
    """
    Represents the guests table in the database.
    
    This class provides methods to access and define columns in the guests table.
    """

    def __init__(self) -> None:
        """
        Initialize the Guests table.
        """
        super().__init__(name='guests')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def firstName(self) -> Column | Self:
        """
        Define the firstName column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='firstName', dataType='text')

    def lastName(self) -> Column | Self:
        """
        Define the lastName column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='lastName', dataType='text')
    
    def email(self) -> Column | Self:
        """
        Define the email column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='email', dataType='text')
    
    def phone(self) -> Column | Self:
        """
        Define the phone column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='phone', dataType='text')
    
    def idCard(self) -> Column | Self:
        """
        Define the idCard column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='idCard', dataType='text')
    
    def nifNumber(self) -> Column | Self:
        """
        Define the nifNumber column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='nifNumber', dataType='text')
    
    def nationality(self) -> Column | Self:
        """
        Define the nationality column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='nationality', dataType='text')
    
    def preferredLanguage(self) -> Column | Self:
        """
        Define the preferredLanguage column of the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        return self._column(name='preferredLanguage', dataType='text')
    
    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Guests: The current instance for method chaining.
        """
        self.id()
        self.firstName()
        self.lastName()
        self.email()
        self.phone()
        self.idCard()
        self.nifNumber()
        self.nationality()
        self.preferredLanguage()
        return self