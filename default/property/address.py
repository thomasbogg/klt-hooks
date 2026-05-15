import re
from typing import Any

from libraries.database.row import Row as DatabaseRow


class Address(DatabaseRow):
    """
    Represents a property address with location details and nearby amenities.
    
    This class handles database operations for property addresses, allowing
    retrieval and modification of location information, street address, coordinates,
    map links, directions, and nearby amenities.
    """
    
    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property address object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertyAddresses')

    @property
    def location(self) -> str | None:
        """
        Get the property location name.
        
        Returns:
            The location name or None if not set.
        """
        return self._get('location')
    
    @location.setter
    def location(self, value: str) -> None:
        """
        Set the property location name.
        
        Args:
            value: The location name to set.
        """
        self._set('location', value)

    @property
    def street(self) -> str | None:
        """
        Get the property street address.
        
        Returns:
            The street address or None if not set.
        """
        return self._get('street')

    @street.setter
    def street(self, value: str) -> None:
        """
        Set the property street address.
        
        Args:
            value: The street address to set.
        """
        self._set('street', value)

    @property
    def postalCode(self) -> str | None:
        """
        Get the property postal code.
        
        Returns:
            The postal code or None if not set.
        """
        return re.search(r'\d{4}-\d{3}', self._get('street')).group(0) if self._get('street') else None
    
    @property
    def city(self) -> str | None:
        """
        Get the property city.
        
        Returns:
            The city name or None if not set.
        """
        return self._get('street').split()[-1] if self._get('street') else None

    @property
    def coordinates(self) -> str | None:
        """
        Get the property GPS coordinates.
        
        Returns:
            The GPS coordinates or None if not set.
        """
        return self._get('coordinates')

    @coordinates.setter
    def coordinates(self, value: str) -> None:
        """
        Set the property GPS coordinates.
        
        Args:
            value: The GPS coordinates to set.
        """
        self._set('coordinates', value)

    @property
    def map(self) -> str | None:
        """
        Get the property map link.
        
        Returns:
            The map link or None if not set.
        """
        return self._get('map')

    @map.setter
    def map(self, value: str) -> None:
        """
        Set the property map link.
        
        Args:
            value: The map link to set.
        """
        self._set('map', value)
    
    @property
    def directions(self) -> str | None:
        """
        Get the directions to the property.
        
        Returns:
            The directions or None if not set.
        """
        return self._get('directions')

    @directions.setter
    def directions(self, value: str) -> None:
        """
        Set the directions to the property.
        
        Args:
            value: The directions to set.
        """
        self._set('directions', value)
    
    @property
    def nearestBins(self) -> str | None:
        """
        Get the location of the nearest waste bins.
        
        Returns:
            The location of nearest bins or None if not set.
        """
        return self._get('nearestBins')

    @nearestBins.setter
    def nearestBins(self, value: str) -> None:
        """
        Set the location of the nearest waste bins.
        
        Args:
            value: The location of nearest bins to set.
        """
        self._set('nearestBins', value)
    
    @property
    def nearestCornerShop(self) -> str | None:
        """
        Get the location of the nearest corner shop.
        
        Returns:
            The location of nearest corner shop or None if not set.
        """
        return self._get('nearestCornerShop')
    
    @nearestCornerShop.setter
    def nearestCornerShop(self, value: str) -> None:
        """
        Set the location of the nearest corner shop.
        
        Args:
            value: The location of nearest corner shop to set.
        """
        self._set('nearestCornerShop', value)
    
    @property
    def nearestSupermarket(self) -> str | None:
        """
        Get the location of the nearest supermarket.
        
        Returns:
            The location of nearest supermarket or None if not set.
        """
        return self._get('nearestSupermarket')
    
    @nearestSupermarket.setter
    def nearestSupermarket(self, value: str) -> None:
        """
        Set the location of the nearest supermarket.
        
        Args:
            value: The location of nearest supermarket to set.
        """
        self._set('nearestSupermarket', value)
    
    def _get_condition(self) -> str:
        """
        Get the database condition to identify this address record.
        
        Returns:
            A SQL condition string based on the location.
        """
        return f'location="{self.location}"'
    
    @property
    def generalLocation(self) -> str:
        """
        Get a general location description for the address.
        
        Returns:
            A string describing the general location, combining street and coordinates.
        """
        location = [item for item in self.location.split() if not item.isdigit()]
        return ' '.join(location)