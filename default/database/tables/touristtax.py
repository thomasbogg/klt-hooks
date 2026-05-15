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
    
    def chargesId(self) -> Column | Self:
        """
        Define the chargesId column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='chargesId', dataType='integer')
    
    def total(self) -> Column | Self:
        """
        Define the total column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='total', dataType='real')
    
    def orderId(self) -> Column | Self:
        """
        Define the orderId column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='orderId', dataType='text')
    
    def orderToken(self) -> Column | Self:
        """
        Define the orderToken column of the table.
        
        Returns:
            Touristtax: The current instance for method chaining.
        """
        return self._column(name='orderToken', dataType='text')
    
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
        self.chargesId()
        self.total()
        self.orderId()
        self.orderToken()
        self.paid()
        return self

    def _get_condition(self) -> str:
        """
        Get the database condition to identify this price record.
        
        Returns:
            A SQL condition string based on the property identifier.
        """
        return f'chargesId="{self._get("chargesId")}"'