from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Touristtax(Table):
    """
    Represents the tourist tax table in the database.
    
    This class provides methods to access and define columns in the tourist tax table.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Touristtax table.
        """
        super().__init__(name='touristtax')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def date(self) -> Column | Self:
        """
        Define the date column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='date', dataType='text')
  
    def orderId(self) -> Column | Self:
        """
        Define the orderId column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='orderId', dataType='text')
    
    def paid(self) -> Column | Self:
        """
        Define the paid column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='paid', dataType='boolean')

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        self.id()
        self.orderId()
        self.date()
        self.paid()
        return self