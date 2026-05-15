from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Charges(Table):
    """
    Represents the charges table in the database.
    
    This class provides methods to access and define columns in the charges table.
    """
    
    def __init__(self) -> None:
        """
        Initialize the Charges table.
        """
        super().__init__(name='charges')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')
    
    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='integer')
    
    def basicRental(self) -> Column | Self:
        """
        Define the basicRental column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='basicRental', dataType='real')
    
    def extraNights(self) -> Column | Self:
        """
        Define the extraNights column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='extraNights', dataType='real')
    
    def currency(self) -> Column | Self:
        """
        Define the currency column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='currency', dataType='text')
    
    def security(self) -> Column | Self:
        """
        Define the security column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='security', dataType='real')
    
    def securityMethod(self) -> Column | Self:
        """
        Define the securityMethod column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='securityMethod', dataType='text')
    
    def admin(self) -> Column | Self:
        """
        Define the admin column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='admin', dataType='real')
    
    def bankTransfer(self) -> Column | Self:
        """
        Define the bankTransfer column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='bankTransfer', dataType='boolean')
    
    def creditCard(self) -> Column | Self:
        """
        Define the creditCard column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='creditCard', dataType='boolean')
    
    def platformFee(self) -> Column | Self:
        """
        Define the platformFee column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='platformFee', dataType='real')
    
    def manualCharges(self) -> Column | Self:
        """
        Define the manualCharges column of the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        return self._column(name='manualCharges', dataType='boolean')
    
    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statement for the charges table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no join is needed.
        """
        joins = []
        if 'bookings' in tableNames:
            joins.append('JOIN charges ON charges.bookingId = bookings.id')
        if 'touristtax' in tableNames:
            joins.append('JOIN touristtax ON touristtax.chargesId = charges.id')
        return joins

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Charges: The current instance for method chaining.
        """
        self.id()
        self.bookingId()
        self.basicRental()
        self.extraNights()
        self.currency()
        self.security()
        self.securityMethod()
        self.admin()
        self.bankTransfer()
        self.creditCard()
        self.platformFee()
        self.manualCharges()
        return self