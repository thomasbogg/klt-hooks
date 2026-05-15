from typing import Any

from libraries.database.row import Row as DatabaseRow


class SEFDetails(DatabaseRow):
    """
    Represents property SEF login data for guest registration.
    
    This class handles database operations for SEF data, including retrieving
    and modifying information such as the Unidade Hoteleira number, estabelecimento,
    and authentication key. It is used to manage SEF-related data for properties.
    It also provides methods to get and set various SEF-related properties.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property SEF data object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertySEFDetails')

    # Identifier properties
    @property
    def propertyId(self) -> int | None:
        """
        Get the associated property's ID.
        
        Returns:
            The property ID or None if not set.
        """
        return self._get('propertyId')
    
    @propertyId.setter
    def propertyId(self, value: int) -> None:
        """
        Set the associated property's ID.
        
        Args:
            value: The property ID to set.
        """
        self._set('propertyId', value)

    # Property status properties
    @property
    def unidadeHoteleira(self) -> bool | None:
        """
        Get the Unidade Hoteleira number for login.
        
        Returns:
            String representing the Unidade Hoteleira number, or None if not set.
        """
        return self._get('unidadeHoteleira')

    @unidadeHoteleira.setter
    def unidadeHoteleira(self, value: str | None) -> None:
        """
        Set the Unidade Hoteleira number for login.
        
        Args:
            value: String representing the Unidade Hoteleira number, or None to unset.
        """
        self._set('unidadeHoteleira', value)

    @property
    def estabelecimento(self) -> str | None:
        """
        Get the Estabelecimento number for login.
        
        Returns:
            String representing the Estabelecimento number, or None if not set.
        """
        return self._get('estabelecimento')

    @estabelecimento.setter
    def estabelecimento(self, value: str | None) -> None:
        """
        Set the Estabelecimento number for login.
        
        Args:
            value: String representing the Estabelecimento number, or None to unset.
        """
        self._set('estabelecimento', value)
    
    @property
    def chaveDeAutenticacao(self) -> str | None:
        """
        Get the authentication key for SEF login.
        
        Returns:
            String representing the authentication key, or None if not set.
        """
        return self._get('chaveDeAutenticacao')
    
    @chaveDeAutenticacao.setter
    def chaveDeAutenticacao(self, value: str | None) -> None:
        """
        Set the authentication key for SEF login.
        
        Args:
            value: String representing the authentication key, or None to unset.
        """
        self._set('chaveDeAutenticacao', value)

    def _get_condition(self) -> str:
        """
        Get the database condition to identify this specification record.
        
        Returns:
            A SQL condition string based on the property ID.
        """
        return f'propertyId = {self.propertyId}'