from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Emails(Table):
    """
    Represents the emails table in the database.
    
    This class provides methods to access and define columns in the emails table.
    """

    def __init__(self) -> None:
        """
        Initialize the Emails table.
        """
        super().__init__(name='emails')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def bookingId(self) -> Column | Self:
        """
        Define the bookingId column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='bookingId', dataType='integer')

    def balancePayment(self) -> Column | Self:
        """
        Define the balancePayment column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='balancePayment', dataType='boolean')

    def arrivalQuestionnaire(self) -> Column | Self:
        """
        Define the arrivalQuestionnaire column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='arrivalQuestionnaire', dataType='boolean')

    def securityDepositRequest(self) -> Column | Self:
        """
        Define the securityDepositRequest column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='securityDepositRequest', dataType='boolean')

    def arrivalInformation(self) -> Column | Self:
        """
        Define the arrivalInformation column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='arrivalInformation', dataType='boolean')

    def guestRegistrationForm(self) -> Column | Self:
        """
        Define the guestRegistrationForm column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='guestRegistrationForm', dataType='boolean')

    def checkInInstructions(self) -> Column | Self:
        """
        Define the checkInInstructions column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='checkInInstructions', dataType='boolean')

    def finalDaysReminder(self) -> Column | Self:
        """
        Define the finalDaysReminder column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='finalDaysReminder', dataType='boolean')

    def goodbye(self) -> Column | Self:
        """
        Define the goodbye column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='goodbye', dataType='boolean')

    def management(self) -> Column | Self:
        """
        Define the management column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='management', dataType='boolean')

    def payOwner(self) -> Column | Self:
        """
        Define the payOwner column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='payOwner', dataType='boolean')

    def securityDepositReturn(self) -> Column | Self:
        """
        Define the securityDepositReturn column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='securityDepositReturn', dataType='boolean')

    def airportTransfers(self) -> Column | Self:
        """
        Define the airportTransfers column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='airportTransfers', dataType='boolean')

    def guestRegistrationFormToOwner(self) -> Column | Self:
        """
        Define the guestRegistrationFormToOwner column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='guestRegistrationFormToOwner', dataType='boolean')

    def paused(self) -> Column | Self:
        """
        Define the paused column of the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        return self._column(name='paused', dataType='boolean')

    def joinStatement(self, tableNames: list[str]) -> list[str]:
        """
        Generate SQL JOIN statement for the emails table.
        
        Parameters:
            tableNames: A list of table names to potentially join with.
            
        Returns:
            A list of JOIN SQL statements or an empty list if no join is needed.
        """
        if 'bookings' in tableNames:
            return ['JOIN emails ON emails.bookingId = bookings.id']
        return []

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Emails: The current instance for method chaining.
        """
        self.id()
        self.bookingId()
        self.balancePayment()
        self.arrivalQuestionnaire()
        self.securityDepositRequest()
        self.arrivalInformation()
        self.guestRegistrationForm()
        self.checkInInstructions()
        self.finalDaysReminder()
        self.goodbye()
        self.management()
        self.payOwner()
        self.securityDepositReturn()
        self.airportTransfers()
        self.guestRegistrationFormToOwner()
        self.paused()
        return self