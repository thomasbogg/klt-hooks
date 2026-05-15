from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Owners(Table):
    """
    Represents the property owners table in the database.
    
    This class provides methods to access and define columns in the propertyOwners table.
    """

    def __init__(self) -> None:
        """
        Initialize the Owners table.
        """
        super().__init__(name='propertyOwners')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def name(self) -> Column | Self:
        """
        Define the name column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='name', dataType='text')

    def email(self) -> Column | Self:
        """
        Define the email column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='email', dataType='text')

    def phone(self) -> Column | Self:
        """
        Define the phone column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='phone', dataType='text')

    def nifNumber(self) -> Column | Self:
        """
        Define the nifNumber column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='nifNumber', dataType='text')

    def defaultClean(self) -> Column | Self:
        """
        Define the defaultClean column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='defaultClean', dataType='boolean')

    def defaultMeetGreet(self) -> Column | Self:
        """
        Define the defaultMeetGreet column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='defaultMeetGreet', dataType='boolean')

    def takesEuros(self) -> Column | Self:
        """
        Define the takesEuros column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='takesEuros', dataType='boolean')

    def takesPounds(self) -> Column | Self:
        """
        Define the takesPounds column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='takesPounds', dataType='boolean')

    def wantsAccounting(self) -> Column | Self:
        """
        Define the wantsAccounting column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='wantsAccounting', dataType='boolean')

    def cleansAreInvoiced(self) -> Column | Self:
        """
        Define the cleansAreInvoiced column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='cleansAreInvoiced', dataType='boolean')

    def rentalCommissionsAreInvoiced(self) -> Column | Self:
        """
        Define the rentalCommissionsAreInvoiced column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='rentalCommissionsAreInvoiced', dataType='boolean')

    def isPaidRegularly(self) -> Column | Self:
        """
        Define the isPaidRegularly column of the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        return self._column(name='isPaidRegularly', dataType='boolean')
    
    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Owners: The current instance for method chaining.
        """
        self.id()
        self.name()
        self.email()
        self.phone()
        self.nifNumber()
        self.defaultClean()
        self.defaultMeetGreet()
        self.takesEuros()
        self.takesPounds()
        self.wantsAccounting()
        self.cleansAreInvoiced()
        self.rentalCommissionsAreInvoiced()
        self.isPaidRegularly()
        return self
