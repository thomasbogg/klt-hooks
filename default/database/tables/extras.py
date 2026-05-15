from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Extras(Table):
    """
    Represents the extras table in the database.
    
    This class provides methods to access and define columns in the extras table.
    """

    def __init__(self) -> None:
        """
        Initialize the Extras table.
        """
        super().__init__(name='extras')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='id', dataType='boolean')
    
    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='boolean')
    
    def airportTransfers(self) -> Column | Self:
        """
        Define the airportTransfers column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='airportTransfers', dataType='boolean')
    
    def airportTransferInboundOnly(self) -> Column | Self:
        """
        Define the airportTransferInboundOnly column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='airportTransferInboundOnly', dataType='boolean')

    def airportTransferOutboundOnly(self) -> Column | Self:
        """
        Define the airportTransferOutboundOnly column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='airportTransferOutboundOnly', dataType='boolean')

    def welcomePack(self) -> Column | Self:
        """
        Define the welcomePack column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='welcomePack', dataType='boolean')
    
    def welcomePackModifications(self) -> Column | Self:
        """
        Define the welcomePackModifications column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='welcomePackModifications', dataType='text')
    
    def cot(self) -> Column | Self:
        """
        Define the cot column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='cot', dataType='boolean')
    
    def highChair(self) -> Column | Self:
        """
        Define the highChair column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='highChair', dataType='boolean')
    
    def midStayClean(self) -> Column | Self:
        """
        Define the midStayClean column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='midStayClean', dataType='boolean')
    
    def lateCheckout(self) -> Column | Self:
        """
        Define the lateCheckout column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='lateCheckout', dataType='boolean')
    
    def otherRequests(self) -> Column | Self:
        """
        Define the otherRequests column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='otherRequests', dataType='text')
    
    def extraNights(self) -> Column | Self:
        """
        Define the extraNights column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='extraNights', dataType='integer')
    
    def childSeats(self) -> Column | Self:
        """
        Define the childSeats column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='childSeats', dataType='text')
    
    def excessBaggage(self) -> Column | Self:
        """
        Define the excessBaggage column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='excessBaggage', dataType='text')
    
    def ownerIsPaying(self) -> Column | Self:
        """
        Define the ownerIsPaying column of the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        return self._column(name='ownerIsPaying', dataType='boolean')

    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statement for the extras table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no join is needed.
        """
        if 'bookings' in tableNames:
            return ['JOIN extras ON extras.bookingId = bookings.id']
        return []

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Extras: The current instance for method chaining.
        """
        self.id()
        self.bookingId()
        self.airportTransfers()
        self.airportTransferInboundOnly()
        self.airportTransferOutboundOnly()
        self.childSeats()
        self.excessBaggage()
        self.welcomePack()
        self.welcomePackModifications()
        self.cot()
        self.highChair()
        self.midStayClean()
        self.lateCheckout()
        self.otherRequests()
        self.extraNights()
        self.ownerIsPaying()
        return self