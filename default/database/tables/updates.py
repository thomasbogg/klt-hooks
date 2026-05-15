from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Updates(Table):
    """
    Represents the updates table in the database.
    
    This class provides methods to access and define columns in the updates table.
    """

    def __init__(self) -> None:
        """
        Initialize the Updates table.
        """
        super().__init__(name='updates')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def date(self) -> Column | Self:
        """
        Define the date column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='date', dataType='text')

    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='integer')

    def details(self) -> Column | Self:
        """
        Define the details column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='details', dataType='text')

    def extras(self) -> Column | Self:
        """
        Define the extras column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='extras', dataType='text')
    
    def messages(self) -> Column | Self:
        """
        Define the messages column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='messages', dataType='text')

    def emailSent(self) -> Column | Self:
        """
        Define the emailSent column of the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        return self._column(name='emailSent', dataType='boolean')
    
    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Updates: The current instance for method chaining.
        """
        self.id()
        self.date()
        self.bookingId()
        self.details()
        self.extras()
        self.messages()
        self.emailSent()
        return self