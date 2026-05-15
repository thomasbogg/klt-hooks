from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Properties(Table):
    """
    Represents the properties table in the database.
    
    This class provides methods to access and define columns in the properties table.
    """

    def __init__(self) -> None:
        """
        Initialize the Properties table.
        """
        super().__init__(name='properties')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def name(self) -> Column | Self:
        """
        Define the name column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='name', dataType='text')

    def shortName(self) -> Column | Self:
        """
        Define the shortName column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='shortName', dataType='text')

    def ownerId(self) -> Column | Self:
        """
        Define the ownerId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='ownerId', dataType='integer')

    def managerId(self) -> Column | Self:
        """
        Define the managerId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='managerId', dataType='integer')

    def addressId(self) -> Column | Self:
        """
        Define the addressId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='addressId', dataType='integer')

    def priceId(self) -> Column | Self:
        """
        Define the priceId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='priceId', dataType='text')

    def accountantId(self) -> Column | Self:
        """
        Define the accountantId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='accountantId', dataType='integer')

    def alNumber(self) -> Column | Self:
        """
        Define the alNumber column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='alNumber', dataType='integer')

    def weBook(self) -> Column | Self:
        """
        Define the weBook column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='weBook', dataType='boolean')

    def bookingComName(self) -> Column | Self:
        """
        Define the bookingComName column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='bookingComName', dataType='text')

    def airbnbName(self) -> Column | Self:
        """
        Define the airbnbName column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='airbnbName', dataType='text')

    def vrboId(self) -> Column | Self:
        """
        Define the vrboId column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='vrboId', dataType='text')

    def weClean(self) -> Column | Self:
        """
        Define the weClean column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='weClean', dataType='boolean')

    def standardCleaningFee(self) -> Column | Self:
        """
        Define the standardCleaningFee column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='standardCleaningFee', dataType='real')

    def sendOwnerBookingForms(self) -> Column | Self:
        """
        Define the sendOwnerBookingForms column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='sendOwnerBookingForms', dataType='boolean')

    def ownerRegistersGuests(self) -> Column | Self:
        """
        Define the ownerRegistersGuests column of the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        return self._column(name='ownerRegistersGuests', dataType='boolean')
    
    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statements for the properties table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements based on the provided table names.
        """
        joins = []
        if 'propertyPrices' in tableNames:
            joins.append('JOIN propertyPrices ON propertyPrices.name = properties.priceId')
        if 'propertyAddresses' in tableNames:
            joins.append('JOIN propertyAddresses ON propertyAddresses.id = properties.addressId')
        if 'propertyAccountants' in tableNames:
            joins.append('JOIN propertyAccountants ON propertyAccountants.id = properties.accountantId')
        if 'propertyManagers' in tableNames:
            joins.append('JOIN propertyManagers ON propertyManagers.id = properties.managerId')
        if 'propertyOwners' in tableNames:
            joins.append('JOIN propertyOwners ON propertyOwners.id = properties.ownerId')
        if 'propertySpecs' in tableNames:
            joins.append('JOIN propertySpecs ON propertySpecs.propertyId = properties.id')
        if 'propertySEFDetails' in tableNames:
            joins.append('JOIN propertySEFDetails ON propertySEFDetails.propertyId = properties.id')
        return joins

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Properties: The current instance for method chaining.
        """
        self.id()
        self.name()
        self.shortName()
        self.ownerId()
        self.managerId()
        self.addressId()
        self.priceId()
        self.accountantId()
        self.alNumber()
        self.weBook()
        self.bookingComName()
        self.airbnbName()
        self.weClean()
        self.standardCleaningFee()
        self.sendOwnerBookingForms()
        self.ownerRegistersGuests()
        return self