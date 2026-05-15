from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Managers(Table):
    """
    Represents the property managers table in the database.
    
    This class provides methods to access and define columns in the propertyManagers table.
    """

    def __init__(self) -> None:
        """
        Initialize the Managers table.
        """
        super().__init__(name='propertyManagers')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def company(self) -> Column | Self:
        """
        Define the company column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='company', dataType='text')

    def name(self) -> Column | Self:
        """
        Define the name column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='name', dataType='text')

    def email(self) -> Column | Self:
        """
        Define the email column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='email', dataType='text')

    def phone(self) -> Column | Self:
        """
        Define the phone column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='phone', dataType='text')

    def maintenance(self) -> Column | Self:
        """
        Define the maintenance column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='maintenance', dataType='text')

    def maintenancePhone(self) -> Column | Self:
        """
        Define the maintenancePhone column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='maintenancePhone', dataType='text')

    def maintenanceEmail(self) -> Column | Self:
        """
        Define the maintenanceEmail column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='maintenanceEmail', dataType='text')

    def liaison(self) -> Column | Self:
        """
        Define the liaison column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='liaison', dataType='text')

    def liaisonPhone(self) -> Column | Self:
        """
        Define the liaisonPhone column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='liaisonPhone', dataType='text')

    def liaisonEmail(self) -> Column | Self:
        """
        Define the liaisonEmail column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='liaisonEmail', dataType='text')

    def cleaning(self) -> Column | Self:
        """
        Define the cleaning column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='cleaning', dataType='text')

    def cleaningPhone(self) -> Column | Self:
        """
        Define the cleaningPhone column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='cleaningPhone', dataType='text')

    def cleaningEmail(self) -> Column | Self:
        """
        Define the cleaningEmail column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='cleaningEmail', dataType='text')
    
    def finance(self) -> Column | Self:
        """
        Define the finance column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='finance', dataType='text')
    
    def financeEmail(self) -> Column | Self:
        """
        Define the financeEmail column of the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        return self._column(name='financeEmail', dataType='text')

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Managers: The current instance for method chaining.
        """
        self.id()
        self.company()
        self.name()
        self.email()
        self.phone()
        self.maintenance()
        self.maintenancePhone()
        self.maintenanceEmail()
        self.liaison()
        self.liaisonPhone()
        self.liaisonEmail()
        self.cleaning()
        self.cleaningPhone()
        self.cleaningEmail()
        self.finance()
        self.financeEmail()
        return self
