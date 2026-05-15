from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Specs(Table):
    """
    Represents the property specifications table in the database.
    
    This class provides methods to access and define columns in the propertySpecs table.
    """

    def __init__(self) -> None:
        """
        Initialize the Specs table.
        """
        super().__init__(name='propertySpecs')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def propertyId(self) -> Column | Self:
        """
        Define the propertyId column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='propertyId', dataType='integer')

    def isListed(self) -> Column | Self:
        """
        Define the isListed column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='isListed', dataType='boolean')

    def isSeaView(self) -> Column | Self:
        """
        Define the isSeaView column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='isSeaView', dataType='boolean')

    def isUpperFloor(self) -> Column | Self:
        """
        Define the isUpperFloor column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='isUpperFloor', dataType='boolean')

    def isBeachfront(self) -> Column | Self:
        """
        Define the isBeachfront column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='isBeachfront', dataType='boolean')

    def bedrooms(self) -> Column | Self:
        """
        Define the bedrooms column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='bedrooms', dataType='integer')

    def bathrooms(self) -> Column | Self:
        """
        Define the bathrooms column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='bathrooms', dataType='integer')

    def squareMetres(self) -> Column | Self:
        """
        Define the squareMetres column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='squareMetres', dataType='integer')
    
    def maxGuests(self) -> Column | Self:
        """
        Define the maxGuests column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='maxGuests', dataType='integer')
    
    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        self.id()
        self.propertyId()
        self.isListed()
        self.isSeaView()
        self.isUpperFloor()
        self.isBeachfront()
        self.bedrooms()
        self.bathrooms()
        self.squareMetres()
        self.maxGuests()
        return self