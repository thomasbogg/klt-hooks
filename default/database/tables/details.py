from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Details(Table):
    """
    Represents the bookings table in the database.
    
    This class provides methods to access and define columns in the bookings table.
    """

    def __init__(self) -> None:
        """
        Initialize the Details table.
        """
        super().__init__(name='bookings')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def propertyId(self) -> Column | Self:
        """
        Define the propertyId column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='propertyId', dataType='integer')
    
    def PIMSId(self) -> Column | Self:
        """
        Define the PIMSId column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='PIMSId', dataType='integer')
    
    def platformId(self) -> Column | Self:
        """
        Define the platformId column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='platformId', dataType='text')
    
    def platformAddress(self) -> Column | Self:
        """
        Define the platformAddress column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='platformAddress', dataType='text')
    
    def guestId(self) -> Column | Self:
        """
        Define the guestId column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='guestId', dataType='integer')
    
    def isOwner(self) -> Column | Self:
        """
        Define the isOwner column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='isOwner', dataType='boolean')
    
    def enquirySource(self) -> Column | Self:
        """
        Define the enquirySource column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='enquirySource', dataType='text')
    
    def enquiryDate(self) -> Column | Self:
        """
        Define the enquiryDate column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='enquiryDate', dataType='text')
    
    def enquiryStatus(self) -> Column | Self:
        """
        Define the enquiryStatus column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='enquiryStatus', dataType='text')
    
    def adults(self) -> Column | Self:
        """
        Define the adults column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='adults', dataType='integer')
    
    def children(self) -> Column | Self:
        """
        Define the children column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='children', dataType='integer')
    
    def babies(self) -> Column | Self:
        """
        Define the babies column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='babies', dataType='integer')
    
    def manualGuests(self) -> Column | Self:
        """
        Define the manualGuests column of the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        return self._column(name='manualGuests', dataType='boolean')
    
    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statements for the bookings table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no joins are needed.
        """
        joins = []
        if 'properties' in tableNames:
            joins.append('JOIN properties ON properties.id = bookings.propertyId')
        if 'guests' in tableNames:
            joins.append('JOIN guests ON guests.id = bookings.guestId')
        return joins

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Details: The current instance for method chaining.
        """
        self.id()
        self.propertyId()
        self.PIMSId()
        self.platformId()
        self.guestId()
        self.isOwner()
        self.enquirySource()
        self.enquiryDate()
        self.enquiryStatus()
        self.adults()
        self.children()
        self.babies()
        self.manualGuests()
        return self