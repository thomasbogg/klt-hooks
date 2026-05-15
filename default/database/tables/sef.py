from libraries.database.column import Column
from libraries.database.table import Table
from typing import Self


class SEFDetails(Table):
    """
    Represents the property sef details table in the database.
    
    This class provides methods to access and define columns in the propertySEFDetails table.
    """

    def __init__(self) -> None:
        """
        Initialize the Specs table.
        """
        super().__init__(name='propertySEFDetails')

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

    def unidadeHoteleira(self) -> Column | Self:
        """
        Define the unidadeHoteleira column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='unidadeHoteleira', dataType='boolean')

    def estabelecimento(self) -> Column | Self:
        """
        Define the estabelecimento column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='estabelecimento', dataType='boolean')

    def chaveDeAutenticacao(self) -> Column | Self:
        """
        Define the chaveDeAutenticacao column of the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        return self._column(name='chaveDeAutenticacao', dataType='boolean')

    def all(self) -> Column | Self:
        """
        Select all columns in the table.
        
        Returns:
            Specs: The current instance for method chaining.
        """
        self.id()
        self.propertyId()
        self.unidadeHoteleira()
        self.estabelecimento()
        self.chaveDeAutenticacao()
        return self