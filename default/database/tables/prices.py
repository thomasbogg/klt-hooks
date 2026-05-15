from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class Prices(Table):
    """
    Represents the property prices table in the database.
    
    This class provides methods to access and define columns in the propertyPrices table.
    """

    def __init__(self) -> None:
        """
        Initialize the Prices table.
        """
        super().__init__(name='propertyPrices')

    def id(self) -> Column | Self:
        """
        Define the id column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='id', dataType='integer')

    def year(self) -> Column | Self:
        """
        Define the year column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='year', dataType='integer')

    def name(self) -> Column | Self:
        """
        Define the name column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='name', dataType='text')
    
    def month(self, monthName: str) -> Column | Self:
        """
        Define a month column of the table.
        
        Parameters:
            monthName: The name of the month.
            
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name=monthName.lower(), dataType='text')

    def january(self) -> Column | Self:
        """
        Define the january column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='january', dataType='real')

    def february(self) -> Column | Self:
        """
        Define the february column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='february', dataType='real')

    def march(self) -> Column | Self:
        """
        Define the march column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='march', dataType='real')

    def april(self) -> Column | Self:
        """
        Define the april column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='april', dataType='real')

    def may(self) -> Column | Self:
        """
        Define the may column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='may', dataType='real')

    def june(self) -> Column | Self:
        """
        Define the june column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='june', dataType='real')

    def july(self) -> Column | Self:
        """
        Define the july column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='july', dataType='real')

    def august(self) -> Column | Self:
        """
        Define the august column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='august', dataType='real')

    def september(self) -> Column | Self:
        """
        Define the september column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='september', dataType='real')

    def october(self) -> Column | Self:
        """
        Define the october column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='october', dataType='real')

    def november(self) -> Column | Self:
        """
        Define the november column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='november', dataType='real')

    def december(self) -> Column | Self:
        """
        Define the december column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='december', dataType='real')
    
    def festive(self) -> Column | Self:
        """
        Define the festive column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='festive', dataType='real')
    
    def earlyWinterMonthlyRate(self) -> Column | Self:
        """
        Define the early winter monthly rate column of the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='earlyWinterMonthlyRate', dataType='real')

    def lateWinterMonthlyRate(self) -> Column | Self:
        """
        Define the late winter monthly rate column of the table.

        Returns:
            Prices: The current instance for method chaining.
        """
        return self._column(name='lateWinterMonthlyRate', dataType='real')

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Prices: The current instance for method chaining.
        """
        self.id()
        self.year()
        self.name()
        self.january()
        self.february()
        self.march()
        self.april()
        self.may()
        self.june()
        self.july()
        self.august()
        self.september()
        self.october()
        self.november()
        self.december()
        self.festive()
        self.earlyWinterMonthlyRate()
        self.lateWinterMonthlyRate()
        return self
