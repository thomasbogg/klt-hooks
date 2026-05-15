from typing import Any

from libraries.database.row import Row as DatabaseRow


class Specs(DatabaseRow):
    """
    Represents property specifications with physical characteristics.
    
    This class handles database operations for property specifications, allowing
    retrieval and modification of information such as size, bedrooms, bathrooms,
    and property features like sea view and beachfront status.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property specifications object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertySpecs')

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
    def isListed(self) -> bool | None:
        """
        Get whether the property is listed for rental.
        
        Returns:
            Boolean indicating if the property is listed, or None if not set.
        """
        return self._get('isListed')

    @isListed.setter
    def isListed(self, value: bool) -> None:
        """
        Set whether the property is listed for rental.
        
        Args:
            value: Boolean indicating if the property is listed.
        """
        self._set('isListed', value)

    # Property feature properties
    @property
    def isSeaView(self) -> bool | None:
        """
        Get whether the property has a sea view.
        
        Returns:
            Boolean indicating if the property has a sea view, or None if not set.
        """
        return self._get('isSeaView')

    @isSeaView.setter
    def isSeaView(self, value: bool) -> None:
        """
        Set whether the property has a sea view.
        
        Args:
            value: Boolean indicating if the property has a sea view.
        """
        self._set('isSeaView', value)

    @property
    def isUpperFloor(self) -> bool | None:
        """
        Get whether the property is on an upper floor.
        
        Returns:
            Boolean indicating if the property is on an upper floor, or None if not set.
        """
        return self._get('isUpperFloor')

    @isUpperFloor.setter
    def isUpperFloor(self, value: bool) -> None:
        """
        Set whether the property is on an upper floor.
        
        Args:
            value: Boolean indicating if the property is on an upper floor.
        """
        self._set('isUpperFloor', value)

    @property
    def isBeachfront(self) -> bool | None:
        """
        Get whether the property is beachfront.
        
        Returns:
            Boolean indicating if the property is beachfront, or None if not set.
        """
        return self._get('isBeachfront')

    @isBeachfront.setter
    def isBeachfront(self, value: bool) -> None:
        """
        Set whether the property is beachfront.
        
        Args:
            value: Boolean indicating if the property is beachfront.
        """
        self._set('isBeachfront', value)

    # Property dimension properties
    @property
    def bedrooms(self) -> int | None:
        """
        Get the number of bedrooms in the property.
        
        Returns:
            The number of bedrooms or None if not set.
        """
        return self._get('bedrooms')

    @bedrooms.setter
    def bedrooms(self, value: int) -> None:
        """
        Set the number of bedrooms in the property.
        
        Args:
            value: The number of bedrooms to set.
        """
        self._set('bedrooms', value)

    @property
    def bathrooms(self) -> float | None:
        """
        Get the number of bathrooms in the property.
        
        Returns:
            The number of bathrooms (float for partial bathrooms) or None if not set.
        """
        return self._get('bathrooms')

    @bathrooms.setter
    def bathrooms(self, value: float) -> None:
        """
        Set the number of bathrooms in the property.
        
        Args:
            value: The number of bathrooms to set (float for partial bathrooms).
        """
        self._set('bathrooms', value)

    @property
    def squareMetres(self) -> int | None:
        """
        Get the size of the property in square metres.
        
        Returns:
            The size in square metres or None if not set.
        """
        return self._get('squareMetres')

    @squareMetres.setter
    def squareMetres(self, value: int) -> None:
        """
        Set the size of the property in square metres.
        
        Args:
            value: The size in square metres to set.
        """
        self._set('squareMetres', value)

    @property
    def maxGuests(self) -> int | None:
        """
        Get the maximum number of guests the property can accommodate.
        
        Returns:
            The maximum number of guests or None if not set.
        """
        return self._get('maxGuests')
    
    @maxGuests.setter
    def maxGuests(self, value: int) -> None:
        """
        Set the maximum number of guests the property can accommodate.
        
        Args:
            value: The maximum number of guests to set.
        """
        self._set('maxGuests', value)
    
    def _get_condition(self) -> str:
        """
        Get the database condition to identify this specification record.
        
        Returns:
            A SQL condition string based on the property ID.
        """
        return f'propertyId = {self.propertyId}'