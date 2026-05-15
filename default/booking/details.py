import datetime

from libraries.database.row import Row as DatabaseRow
from default.dates import dates
from default.property.property import Property
from default.settings import (
    PLATFORMS,
    VALID_BOOKING_STATUSES,
)


class Details(DatabaseRow):
    """
    Represents the primary booking details for a property rental.
    
    This class stores core information about a booking including property details,
    guest information, booking status, and guest counts.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Details instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, tablename='bookings')
        self._propertyName = None
    
    # Primary identifiers
    @property
    def id(self) -> int | None:
        """
        Get the booking ID.
        
        Returns:
            The unique identifier for this booking
        """
        return self._get('id')
            
    @id.setter
    def id(self, value: int) -> None:
        """
        Set the booking ID.
        
        Args:
            value: The ID to set
        """
        self._set('id', value)

    @property
    def propertyId(self) -> int | None:
        """
        Get the property ID associated with this booking.
        
        Returns:
            The ID of the property
        """
        return self._get('propertyId')

    @propertyId.setter
    def propertyId(self, propertyNameOrId: int | str) -> None:
        """
        Set the property ID by ID or name lookup.
        
        Args:
            propertyNameOrId: The property ID or name to set
        """
        if isinstance(propertyNameOrId, int):
            self._set('propertyId', propertyNameOrId)
            return
        
        self._propertyName = propertyNameOrId
        self._set('propertyId', self.getForeignKeyId(Property, 'name', propertyNameOrId))

    @property
    def propertyName(self) -> str | None:
        """
        Get the property name.
        
        Returns:
            The name of the property
        """
        return self._propertyName
    
    @property
    def PIMSId(self) -> int | None:
        """
        Get the PIMS system ID for this booking.
        
        Returns:
            The PIMS system identifier
        """
        return self._get('PIMSId')
            
    @PIMSId.setter
    def PIMSId(self, value: int | str | None) -> None:
        """
        Set the PIMS system ID.
        
        Args:
            value: The PIMS ID to set
        """
        if value is None:
            self._set('PIMSId', None)
            return
        self._set('PIMSId', int(value))

    @property
    def platformId(self) -> str | None:
        """
        Get the platform-specific ID for this booking.
        
        Returns:
            The platform-specific identifier
        """
        return self._get('platformId')
    
    @property
    def platformIdStripped(self) -> str | None:
        """
        Get the platform ID with whitespace stripped.
        
        Returns:
            The stripped platform ID
        """
        platformId = self.platformId
        if not platformId:
            return None
        if self.enquirySource == 'Booking.com':
            platformId = platformId.split('-')[0]
        return platformId.strip()

    @platformId.setter
    def platformId(self, value: str | None) -> None:
        """
        Set the platform-specific ID.
        
        Args:
            value: The platform ID to set
        """
        self._set('platformId', value)

    @property
    def platformAddress(self) -> str | None:
        """
        Get the platform address for this booking.
        
        Returns:
            The platform address (e.g., URL or listing name)
        """
        return self._get('platformAddress')
    
    @platformAddress.setter
    def platformAddress(self, value: str | None) -> None:
        """
        Set the platform address.
        
        Args:
            value: The platform address to set
        """
        self._set('platformAddress', value)
    
    @property
    def guestId(self) -> int | None:
        """
        Get the guest ID associated with this booking.
        
        Returns:
            The ID of the guest
        """
        return self._get('guestId')
    
    @guestId.setter
    def guestId(self, value: int) -> None:
        """
        Set the guest ID.
        
        Args:
            value: The guest ID to set
        """
        self._set('guestId', value)

    # Booking details
    @property
    def isOwner(self) -> bool | None:
        """
        Check if the booking is made by the owner.
        
        Returns:
            True if the booking is made by the property owner, False otherwise
        """
        return self._get('isOwner')

    @isOwner.setter
    def isOwner(self, value: bool) -> None:
        """
        Set whether the booking is made by the owner.
        
        Args:
            value: True if the booking is made by the property owner
        """
        self._set('isOwner', value)

    @property
    def enquirySource(self) -> str | None:
        """
        Get the source of the booking enquiry.
        
        Returns:
            The source of the booking (e.g., 'Direct', 'Airbnb', etc.)
        """
        return self._get('enquirySource') 
            
    @enquirySource.setter
    def enquirySource(self, value: str) -> None:
        """
        Set the source of the booking enquiry.
        
        Args:
            value: The source of the booking
        """
        self._set('enquirySource', value)

    @property
    def enquiryDate(self) -> datetime.date | None:
        """
        Get the date when the booking enquiry was made.
        
        Returns:
            The date of the booking enquiry
        """
        return self._get('enquiryDate')
            
    @enquiryDate.setter
    def enquiryDate(self, value: datetime.date) -> None:
        """
        Set the date when the booking enquiry was made.
        
        Args:
            value: The enquiry date to set
        """
        self._set('enquiryDate', value)

    @property
    def enquiryStatus(self) -> str | None:
        """
        Get the status of the booking enquiry.
        
        Returns:
            The status of the booking (e.g., 'Confirmed', 'Pending', etc.)
        """
        return self._get('enquiryStatus')
            
    @enquiryStatus.setter
    def enquiryStatus(self, value: str) -> None:
        """
        Set the status of the booking enquiry.
        
        Args:
            value: The enquiry status to set
        """
        self._set('enquiryStatus', value)

    # Guest information
    @property
    def adults(self) -> int | None:
        """
        Get the number of adults in the booking.
        
        Returns:
            The number of adult guests
        """
        return self._get('adults') 
            
    @adults.setter
    def adults(self, value: int | None) -> None:
        """
        Set the number of adults in the booking.
        
        Args:
            value: The number of adult guests to set
        """
        self._set('adults', value)
    
    @adults.deleter
    def adults(self) -> None:
        """
        Remove the adults count from the booking.
        """
        self._set('adults', None)

    @property
    def children(self) -> int | None:
        """
        Get the number of children in the booking.
        
        Returns:
            The number of child guests
        """
        return self._get('children') 

    @children.setter
    def children(self, value: int | None) -> None:
        """
        Set the number of children in the booking.
        
        Args:
            value: The number of child guests to set
        """
        self._set('children', value)
    
    @children.deleter
    def children(self) -> None:
        """
        Remove the children count from the booking.
        """
        self._set('children', None)

    @property
    def babies(self) -> int | None:
        """
        Get the number of babies in the booking.
        
        Returns:
            The number of baby guests
        """
        return self._get('babies') 

    @babies.setter
    def babies(self, value: int | None) -> None:
        """
        Set the number of babies in the booking.
        
        Args:
            value: The number of baby guests to set
        """
        self._set('babies', value)

    @babies.deleter
    def babies(self) -> None:
        """
        Remove the babies count from the booking.
        """
        self._set('babies', None)
    
    @property
    def manualGuests(self) -> bool | None:
        """
        Check if guest counts were manually entered.
        
        Returns:
            True if guest counts were manually entered, False otherwise
        """
        return self._get('manualGuests')

    @manualGuests.setter
    def manualGuests(self, value: bool) -> None:
        """
        Set whether guest counts were manually entered.
        
        Args:
            value: True if guest counts were manually entered
        """
        self._set('manualGuests', value)
    
    @property
    def lastUpdated(self) -> datetime.datetime | None:
        """
        Get the date when the booking was last updated.
        
        Returns:
            The date of the last update
        """
        return self._get('lastUpdated')
    
    @lastUpdated.setter
    def lastUpdated(self, value: datetime.datetime) -> None:
        """
        Set the date when the booking was last updated.
        
        Args:
            value: The update date to set
        """
        self._set('lastUpdated', value)
    
    # Calculated properties
    @property
    def statusIsOkay(self) -> bool:
        """
        Check if the booking status is valid.
        
        Returns:
            True if the booking status is in the list of valid statuses
        """
        return self.enquiryStatus in VALID_BOOKING_STATUSES
    
    @property
    def managementStatusIsOkay(self) -> bool:
        """
        Check if the management booking status is valid.
        
        Returns:
            True if the management booking status is in the list of valid statuses
        """
        return self.enquiryStatus == 'Booking confirmed as replacement' or self.statusIsOkay
    
    @property
    def statusIsNotOkay(self) -> bool:
        """
        Check if the booking status is invalid.
        
        Returns:
            True if the booking status is not in the list of valid statuses
        """
        return not self.statusIsOkay
    
    @property
    def prettyGuests(self) -> str:
        """
        Get a formatted string representation of guest counts.
        
        Returns:
            A formatted string like "2A 1C 1B" for 2 adults, 1 child, 1 baby
        """
        if not self.adults:
            return 'Unk. Guests'
        string = f'{self.adults}A'
        if self.children:
            string += f' {self.children}C'
        if self.babies:
            string += f' {self.babies}B'
        return string
    
    @property
    def totalGuests(self) -> int:
        """
        Calculate the total number of guests.
        
        Returns:
            The sum of adults, children, and babies
        """
        total = 0
        if self.adults:
            total += self.adults
        if self.children:
            total += self.children
        if self.babies:
            total += self.babies
        return total
    
    @property
    def prettyEnquiryDate(self) -> str | None:
        """
        Get a formatted string representation of the enquiry date.
        
        Returns:
            A formatted date string or None if the enquiry date is not set
        """
        return dates.prettyDate(self.enquiryDate)
    
    @property
    def isPlatform(self) -> bool:
        """
        Check if the booking comes from a third-party platform.
        
        Returns:
            True if the booking is from a platform like Airbnb, Booking.com, etc.
        """
        return self.enquirySource in PLATFORMS
    
    def exists(self) -> bool:
        """
        Check if this booking already exists in the database.
        Tries to find the booking by ID, PIMSId, or platformId.
        
        Returns:
            True if the booking exists in the database, False otherwise
        """
        # Check by ID
        try:
            if self.id:
                return True
        except KeyError:
            pass
        
        # Check by PIMSId
        try:
            if self.PIMSId:
                result = self.database.runSQL(
                    f'SELECT id FROM bookings WHERE PIMSId = {self.PIMSId}'
                )._cursor.fetchone()
                if result:
                    self.id = result[0]
                    return True
        except (AttributeError, TypeError, KeyError):
            pass
        
        # Check by platformId
        try:
            if self.platformId:
                result = self.database.runSQL(
                    f'SELECT id FROM bookings WHERE platformId = "{self.platformId}"'
                )._cursor.fetchone()
                if result:
                    self.id = result[0]
                    return True
        except (AttributeError, TypeError, KeyError):
            pass
            
        return False