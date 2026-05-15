from typing import Any

from libraries.database.row import Row as DatabaseRow
from default.property.accountant import Accountant
from default.property.address import Address
from default.property.manager import Manager
from default.property.owner import Owner
from default.property.prices import Prices
from default.property.sef import SEFDetails
from default.property.specs import Specs


class Property(DatabaseRow):
    """
    Represents a property with its associated details and relationships.
    
    This class handles database operations for properties, allowing retrieval 
    and modification of property information, and provides access to related
    entities such as owner, manager, address, accountant, and pricing details.
    """
    
    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property object with related components.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'properties')
        self._specs = Specs(database)
        self._owner = Owner(database)
        self._manager = Manager(database)
        self._address = Address(database)
        self._accountant = Accountant(database)
        self._prices = Prices(database)
        self._sef = SEFDetails(database)

    # Basic property information
    @property
    def name(self) -> str | None:
        """
        Get the full name of the property.
        
        Returns:
            The property name or None if not set.
        """
        return self._get('name')

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the full name of the property.
        
        Args:
            value: The property name to set.
        """
        self._set('name', value)

    @property
    def shortName(self) -> str | None:
        """
        Get the short name of the property.
        
        Returns:
            The shortened property name or None if not set.
        """
        return self._get('shortName')
    
    @shortName.setter
    def shortName(self, value: str) -> None:
        """
        Set the short name of the property.
        
        Args:
            value: The shortened property name to set.
        """
        self._set('shortName', value)
    
    @property
    def alNumber(self) -> str | None:
        """
        Get the property's Alojamento Local (AL) registration number.
        
        Returns:
            The AL registration number or None if not set.
        """
        return self._get('alNumber')
    
    @alNumber.setter
    def alNumber(self, value: str) -> None:
        """
        Set the property's Alojamento Local (AL) registration number.
        
        Args:
            value: The AL registration number to set.
        """
        self._set('alNumber', value)

    # Related entities IDs
    @property
    def ownerId(self) -> int | None:
        """
        Get the property owner's ID.
        
        Returns:
            The owner ID or None if not set.
        """
        return self._get('ownerId')

    @ownerId.setter
    def ownerId(self, value: int) -> None:
        """
        Set the property owner's ID.
        
        Args:
            value: The owner ID to set.
        """
        self._set('ownerId', value)
    
    @property
    def managerId(self) -> int | None:
        """
        Get the property manager's ID.
        
        Returns:
            The manager ID or None if not set.
        """
        return self._get('managerId')

    @managerId.setter
    def managerId(self, value: int) -> None:
        """
        Set the property manager's ID.
        
        Args:
            value: The manager ID to set.
        """
        self._set('managerId', value)

    @property
    def addressId(self) -> int | None:
        """
        Get the property address ID.
        
        Returns:
            The address ID or None if not set.
        """
        return self._get('addressId')

    @addressId.setter
    def addressId(self, value: int) -> None:
        """
        Set the property address ID.
        
        Args:
            value: The address ID to set.
        """
        self._set('addressId', value)

    @property
    def accountantId(self) -> int | None:
        """
        Get the property accountant's ID.
        
        Returns:
            The accountant ID or None if not set.
        """
        return self._get('accountantId')

    @accountantId.setter
    def accountantId(self, value: int) -> None:
        """
        Set the property accountant's ID.
        
        Args:
            value: The accountant ID to set.
        """
        self._set('accountantId', value)

    @property
    def priceId(self) -> int | None:
        """
        Get the property price schedule ID.
        
        Returns:
            The price schedule ID or None if not set.
        """
        return self._get('priceId')

    @priceId.setter
    def priceId(self, value: int) -> None:
        """
        Set the property price schedule ID.
        
        Args:
            value: The price schedule ID to set.
        """
        self._set('priceId', value)

    # Booking platform identifiers
    @property
    def bookingComName(self) -> str | None:
        """
        Get the property's Booking.com identifier.
        
        Returns:
            The Booking.com identifier or None if not set.
        """
        return self._get('bookingComName')

    @bookingComName.setter
    def bookingComName(self, value: str) -> None:
        """
        Set the property's Booking.com identifier.
        
        Args:
            value: The Booking.com identifier to set.
        """
        self._set('bookingComName', value)

    @property
    def airbnbName(self) -> str | None:
        """
        Get the property's Airbnb identifier.
        
        Returns:
            The Airbnb identifier or None if not set.
        """
        return self._get('airbnbName')

    @airbnbName.setter
    def airbnbName(self, value: str) -> None:
        """
        Set the property's Airbnb identifier.
        
        Args:
            value: The Airbnb identifier to set.
        """
        self._set('airbnbName', value)

    @property
    def vrboId(self) -> str | None:
        """
        Get the property's VRBO identifier.
        
        Returns:
            The VRBO identifier or None if not set.
        """
        return self._get('vrboId')

    @vrboId.setter
    def vrboId(self, value: str) -> None:
        """
        Set the property's VRBO identifier.
        
        Args:
            value: The VRBO identifier to set.
        """
        self._set('vrboId', value)
    
    # Management settings
    @property
    def standardCleaningFee(self) -> float | None:
        """
        Get the standard cleaning fee for the property.
        
        Returns:
            The standard cleaning fee or None if not set.
        """
        return self._get('standardCleaningFee')

    @standardCleaningFee.setter
    def standardCleaningFee(self, value: float) -> None:
        """
        Set the standard cleaning fee for the property.
        
        Args:
            value: The standard cleaning fee to set.
        """
        self._set('standardCleaningFee', value)

    @property
    def weClean(self) -> bool | None:
        """
        Get whether we provide cleaning services for the property.
        
        Returns:
            Boolean indicating if we clean the property, or None if not set.
        """
        return self._get('weClean')

    @weClean.setter
    def weClean(self, value: bool) -> None:
        """
        Set whether we provide cleaning services for the property.
        
        Args:
            value: Boolean indicating if we clean the property.
        """
        self._set('weClean', value)
    
    @property
    def weBook(self) -> bool | None:
        """
        Get whether we manage bookings for the property.
        
        Returns:
            Boolean indicating if we manage bookings, or None if not set.
        """
        return self._get('weBook')

    @weBook.setter
    def weBook(self, value: bool) -> None:
        """
        Set whether we manage bookings for the property.
        
        Args:
            value: Boolean indicating if we manage bookings.
        """
        self._set('weBook', value)
    
    @property
    def ownerRegistersGuests(self) -> bool | None:
        """
        Get whether the owner handles guest registration.
        
        Returns:
            Boolean indicating if owner registers guests, or None if not set.
        """
        return self._get('ownerRegistersGuests')

    @ownerRegistersGuests.setter
    def ownerRegistersGuests(self, value: bool) -> None:
        """
        Set whether the owner handles guest registration.
        
        Args:
            value: Boolean indicating if owner registers guests.
        """
        self._set('ownerRegistersGuests', value)

    @property
    def sendOwnerBookingForms(self) -> bool | None:
        """
        Get whether booking forms are sent to the owner.
        
        Returns:
            Boolean indicating if booking forms are sent to owner, or None if not set.
        """
        return self._get('sendOwnerBookingForms')

    @sendOwnerBookingForms.setter
    def sendOwnerBookingForms(self, value: bool) -> None:
        """
        Set whether booking forms are sent to the owner.
        
        Args:
            value: Boolean indicating if booking forms should be sent to owner.
        """
        self._set('sendOwnerBookingForms', value)

    # Related entity access properties
    @property
    def sefDetails(self) -> SEFDetails:
        """
        Get the SEF details object for the property.
        
        Returns:
            The associated SEFDetails object.
        """
        return self._sef
    
    @property
    def specs(self) -> Specs:
        """
        Get the property specifications object.
        
        Returns:
            The associated Specs object.
        """
        return self._specs
    
    @property
    def owner(self) -> Owner:
        """
        Get the property owner object.
        
        Returns:
            The associated Owner object.
        """
        return self._owner
    
    @property
    def manager(self) -> Manager:
        """
        Get the property manager object.
        
        Returns:
            The associated Manager object.
        """
        return self._manager
    
    @property
    def address(self) -> Address:
        """
        Get the property address object.
        
        Returns:
            The associated Address object.
        """
        return self._address
    
    @property
    def accountant(self) -> Accountant:
        """
        Get the property accountant object.
        
        Returns:
            The associated Accountant object.
        """
        return self._accountant
    
    @property
    def prices(self) -> Prices:
        """
        Get the property prices object.
        
        Returns:
            The associated Prices object.
        """
        return self._prices
    
    # Property type identifiers
    @property
    def isClubeDoMonaco(self) -> bool:
        """
        Check if the property is in Clube do Monaco.
        
        Returns:
            True if the property is in Clube do Monaco, False otherwise.
        """
        return 'clube do monaco' in self.name.lower() if self.name else False
    
    @property
    def isQuintaDaBarracuda(self) -> bool:
        """
        Check if the property is in Quinta da Barracuda.
        
        Returns:
            True if the property is in Quinta da Barracuda, False otherwise.
        """
        return 'quinta da barracuda' in self.name.lower() if self.name else False
    
    @property
    def isParqueDaCorcovada(self) -> bool:
        """
        Check if the property is in Parque da Corcovada.
        
        Returns:
            True if the property is in Parque da Corcovada, False otherwise.
        """
        return 'parque da corcovada' in self.name.lower() if self.name else False
    
    @property
    def isCerroMar(self) -> bool:
        """
        Check if the property is in Cerro Mar.
        
        Returns:
            True if the property is in Cerro Mar, False otherwise.
        """
        return 'cerro mar' in self.name.lower() if self.name else False
    
    @property
    def bookingComId(self) -> str | None:
        """
        Get the property complex's Booking.com identifier.
        
        Returns:
            The property complex's Booking.com ID based on location, or None if not recognized.
        """
        if self.isQuintaDaBarracuda:
            return '8715453'
        if self.isClubeDoMonaco:
            return '8252517'
        if self.isParqueDaCorcovada:
            return '9330221'
        return None

    # Data handling
    def set(self, load: dict) -> 'Property':
        """
        Set properties from a dictionary including related entities.
        
        Args:
            load: Dictionary containing property data and related entity data.
            
        Returns:
            Self for method chaining.
        """
        if 'propertySpecs' in load:
            self.specs.set(load['propertySpecs'])
        if 'propertyOwners' in load:
            self.owner.set(load['propertyOwners'])
        if 'propertyManagers' in load:
            self.manager.set(load['propertyManagers'])
        if 'propertyAddresses' in load:
            self.address.set(load['propertyAddresses'])
        if 'propertyAccountants' in load:
            self.accountant.set(load['propertyAccountants'])
        if 'propertyPrices' in load:
            self.prices.set(load['propertyPrices'])
        if 'propertySEFDetails' in load:
            self.sefDetails.set(load['propertySEFDetails'])
        return super().set(load)

    def _get_condition(self) -> str | None:
        """
        Get the database condition to identify this property record.
        
        Returns:
            A SQL condition string based on name or short name, or None if neither is set.
        """
        if hasattr(self, 'name') and self.name:
            return f'name="{self.name}"'
        if 'shortName' in self._values:
            return f'shortName="{self.shortName}"'
        return None
