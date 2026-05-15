from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Forms(Table):
    """
    Represents the forms table in the database.
    
    This class provides methods to access and define columns in the forms table.
    """

    def __init__(self) -> None:
        """
        Initialize the Forms table.
        """
        super().__init__(name='forms')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='integer')

    def balancePayment(self) -> Column | Self:
        """
        Define the balancePayment column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='balancePayment', dataType='text')

    def arrivalQuestionnaire(self) -> Column | Self:
        """
        Define the arrivalQuestionnaire column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='arrivalQuestionnaire', dataType='text')

    def guestRegistration(self) -> Column | Self:
        """
        Define the guestRegistration column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='guestRegistration', dataType='text')

    def guestRegistrationDone(self) -> Column | Self:
        """
        Define the guestRegistrationDone column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='guestRegistrationDone', dataType='boolean')

    def securityDeposit(self) -> Column | Self:
        """
        Define the securityDeposit column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='securityDeposit', dataType='text')

    def PIMSuin(self) -> Column | Self:
        """
        Define the PIMSuin column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='PIMSuin', dataType='text')

    def PIMSoid(self) -> Column | Self:
        """
        Define the PIMSoid column of the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        return self._column(name='PIMSoid', dataType='text')
    
    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statement for the forms table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no join is needed.
        """
        if 'bookings' in tableNames:
            return ['JOIN forms ON forms.bookingId = bookings.id']
        return []

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Forms: The current instance for method chaining.
        """
        self.id()
        self.bookingId()
        self.balancePayment()
        self.arrivalQuestionnaire()
        self.guestRegistration()
        self.guestRegistrationDone()
        self.securityDeposit()
        self.PIMSuin()
        self.PIMSoid()
        return self
