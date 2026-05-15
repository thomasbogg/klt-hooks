from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Departures(Table):
    """
    Represents the departures table in the database.
    
    This class provides methods to access and define columns in the departures table.
    """

    def __init__(self) -> None:
        """
        Initialize the Departures table.
        """
        super().__init__(name='departures')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='integer')
    
    def date(self) -> Column | Self:
        """
        Define the date column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='date', dataType='text')
    
    def flightNumber(self) -> Column | Self:
        """
        Define the flightNumber column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='flightNumber', dataType='text')
    
    def isFaro(self) -> Column | Self:
        """
        Define the isFaro column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='isFaro', dataType='boolean')
    
    def time(self) -> Column | Self:
        """
        Define the time column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='time', dataType='text')
    
    def details(self) -> Column | Self:
        """
        Define the details column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='details', dataType='text')
    
    def clean(self) -> Column | Self:
        """
        Define the clean column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='clean', dataType='boolean')
    
    def manualDate(self) -> Column | Self:
        """
        Define the manualDate column of the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        return self._column(name='manualDate', dataType='boolean')
    
    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statement for the departures table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no join is needed.
        """
        if 'bookings' in tableNames:
            return ['JOIN departures ON bookings.id = departures.bookingId']
        return []

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Departures: The current instance for method chaining.
        """
        self.id()
        self.bookingId()
        self.date()
        self.flightNumber()
        self.isFaro()
        self.time()
        self.details()
        self.clean()
        self.manualDate()
        return self