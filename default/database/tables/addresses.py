from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Addresses(Table):
    """
    Represents the property addresses table in the database.
    
    This class provides methods to access and define columns in the propertyAddresses table.
    """

    def __init__(self) -> None:
        """
        Initialize the Addresses table.
        """
        super().__init__(name='propertyAddresses')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def location(self) -> Column | Self:
        """
        Define the location column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='location', dataType='text')

    def street(self) -> Column | Self:
        """
        Define the street column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='street', dataType='text')

    def coordinates(self) -> Column | Self:
        """
        Define the coordinates column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='coordinates', dataType='text')

    def map(self) -> Column | Self:
        """
        Define the map column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='map', dataType='text')

    def directions(self) -> Column | Self:
        """
        Define the directions column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='directions', dataType='text')

    def nearestBins(self) -> Column | Self:
        """
        Define the nearestBins column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='nearestBins', dataType='text')
    
    def nearestCornerShop(self) -> Column | Self:
        """
        Define the nearestCornerShop column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='nearestCornerShop', dataType='text')
    
    def nearestSupermarket(self) -> Column | Self:
        """
        Define the nearestSupermarket column of the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        return self._column(name='nearestSupermarket', dataType='text')

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Addresses: The current instance for method chaining.
        """
        self.id()
        self.location()
        self.street()
        self.coordinates()
        self.map()
        self.directions()
        self.nearestBins()
        self.nearestCornerShop()
        self.nearestSupermarket()
        return self