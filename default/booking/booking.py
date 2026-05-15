from datetime import date

from default.booking.arrival import Arrival
from default.booking.charges import Charges
from default.booking.touristtax import Touristtax
from default.booking.departure import Departure
from default.booking.details import Details
from default.booking.emails import Emails
from default.booking.extras import Extras
from default.booking.forms import Forms
from default.dates import dates
from default.guest.guest import Guest
from default.property.property import Property
from default.settings import PLATFORMS
from typing import Any
from libraries.utils import logerror


class Booking:
    """
    The main Booking class that represents a complete booking record in the system.
    This class composes all aspects of a booking including guest details, property information,
    arrival/departure details, charges, extras, emails, and forms.
    """
    
    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a new Booking instance with all required components.
        
        Args:
            database: The database connection to use for database operations
        """
        self._database = database
        self._details = Details(database)
        self._arrival = Arrival(database)
        self._departure = Departure(database)
        self._charges = Charges(database)
        self._extras = Extras(database)
        self._emails = Emails(database)
        self._touristtax = Touristtax(database)
        self._forms = Forms(database)
        self._property = Property(database)
        self._guest = Guest(database)

    @property
    def id(self) -> int | None:
        """
        Get the unique identifier for this booking.
        
        Returns:
            The booking ID if it exists, None otherwise
        """
        return self._details.id
        
    @property
    def statusIsOkay(self) -> bool:
        """
        Check if the booking status is in an 'okay' state.
        
        Returns:
            True if the booking status is okay, False otherwise
        """
        return self._details.statusIsOkay
    
    @property
    def statusIsNotOkay(self) -> bool:
        """
        Check if the booking status is not in an 'okay' state.
        
        Returns:
            True if the booking status is not okay, False otherwise
        """
        return self._details.statusIsNotOkay
    
    @property
    def managementStatusIsOkay(self) -> bool:
        """
        Check if the management booking status is valid.
        
        Returns:
            True if the management booking status is in the list of valid statuses
        """
        return self._details.managementStatusIsOkay
    

    @property
    def totalNights(self) -> int:
        """
        Calculate the total number of nights for this booking.
        
        Returns:
            Number of nights between arrival and departure dates
        """
        return dates.subtractDates(self._arrival.date, self._departure.date)

    @property
    def totalGuests(self) -> int:
        """
        Get the total number of guests for this booking.
        
        Returns:
            Total number of guests (adults + children + babies)
        """
        return self._details.totalGuests
    
    @property
    def shouldBePounds(self) -> bool:
        """
        Determine if the booking should be processed in British Pounds.
        
        Returns:
            True if the booking should be in GBP, False otherwise
        """
        if self._property.owner.takesPounds and self._property.owner.takesEuros:
            return self._charges.currency == 'GBP'
        return False
    
    @property
    def shouldBeEuros(self) -> bool:
        """
        Determine if the booking should be processed in Euros.
        
        Returns:
            True if the booking should be in EUR, False otherwise
        """
        return not self.shouldBePounds
    
    @property
    def paymentToOwnerDate(self) -> date:
        """
        Calculate the date when payment should be made to the property owner.
        
        Returns:
            The date when payment is due to the property owner (3 days after arrival)
        """
        return dates.calculate(date=self.arrival.date, days=3)
    
    @property
    def isPlatform(self) -> bool:
        """
        Determine if the booking was made through a third-party platform.
        
        Returns:
            True if the booking came from a platform like Airbnb, Booking.com, etc.
        """
        return self._details.enquirySource in PLATFORMS
    
    @property
    def details(self) -> Details:
        """
        Get the booking details component.
        
        Returns:
            The booking details object
        """
        return self._details

    @property
    def arrival(self) -> Arrival:
        """
        Get the arrival information component.
        
        Returns:
            The arrival details object
        """
        return self._arrival

    @property
    def departure(self) -> Departure:
        """
        Get the departure information component.
        
        Returns:
            The departure details object
        """
        return self._departure

    @property
    def charges(self) -> Charges:
        """
        Get the charges and fees component.
        
        Returns:
            The charges details object
        """
        return self._charges

    @property
    def extras(self) -> Extras:
        """
        Get the booking extras component.
        
        Returns:
            The extras details object
        """
        return self._extras

    @property
    def emails(self) -> Emails:
        """
        Get the email tracking component.
        
        Returns:
            The email tracking object
        """
        return self._emails
    
    @property
    def forms(self) -> Forms:
        """
        Get the forms component.
        
        Returns:
            The forms tracking object
        """
        return self._forms
    
    @property
    def guest(self) -> Guest:
        """
        Get the guest information component.
        
        Returns:
            The guest details object
        """
        return self._guest
    
    @guest.setter
    def guest(self, guest: Guest) -> None:
        """
        Set the guest information component.
        
        Args:
            guest: The guest details object to set
        """
        self._guest = guest

    @property
    def property(self) -> Property:
        """
        Get the property information component.
        
        Returns:
            The property details object
        """
        return self._property

    def set(self, load: dict[str, Any] | None) -> 'Booking':
        """
        Set booking data from a dictionary of values loaded from the database.
        
        Args:
            load: Dictionary containing booking data organized by table names
            
        Returns:
            Self for method chaining
        """
        if load is None:
            return self
        if 'bookings' in load:
            self._details.set(load['bookings'])
        if 'arrivals' in load:
            self._arrival.set(load['arrivals'])
        if 'departures' in load:
            self._departure.set(load['departures'])
        if 'charges' in load:
            self._charges.set(load)
        if 'extras' in load:
            self._extras.set(load['extras'])
        if 'emails' in load:
            self._emails.set(load['emails'])
        if 'forms' in load:
            self._forms.set(load['forms'])
        if 'properties' in load:
            self._property.set(load)
        if 'guests' in load:
            self._guest.set(load['guests'])
        return self
    
    def get(self) -> dict[str, dict[str, Any]]:
        """
        Get all booking data as a nested dictionary.
        
        Returns:
            Dictionary containing all booking data organized by component
        """
        return {
            'details': self._details.get(),
            'arrival': self._arrival.get(),
            'departure': self._departure.get(),
            'charges': self._charges.get(),
            'extras': self._extras.get(),
            'emails': self._emails.get(),
            'forms': self._forms.get(),
            'property': self._property.get(),
            'guest': self._guest.get(),
        }

    def insert(self) -> 'Booking':
        """
        Insert a new booking record into the database.
        First inserts or updates the guest record, then inserts the booking details,
        followed by all other booking components.
        
        Returns:
            Self for method chaining
        """
        if self._guest.exists():
            self._details.guestId = self._guest.id
           
            if self._guest.hasNewDetails():
                self._guest.update()
        else:
            self._details.guestId = self._guest.insert()
        
        self._details.lastUpdated = dates.now()
        bookingId = self._details.insert()
        self._details.id = bookingId
        self._set_booking_id(bookingId)
        
        self._arrival.insert()
        self._departure.insert()
        self._charges.insert()
        self._extras.insert()
        self._emails.insert()
        self._forms.insert()
        self._touristtax.insert()
        return self
    
    def save(self) -> 'Booking':
        """
        Save the booking to the database, either by updating an existing record
        or inserting a new one.
        
        Returns:
            Self for method chaining
        """
        if self.exists():
            return self.update()
        return self.insert()

    def update(self) -> 'Booking':
        """
        Update an existing booking record in the database.
        First updates the guest record if needed, then updates all booking components.
        
        Returns:
            Self for method chaining
        """
        self._guest.id = self._details.guestId
      
        if self._guest.hasNewDetails():
            self._guest.update()
      
        self._details.update()
        self._set_booking_id(self._details.id)
        self._arrival.update()
        self._departure.update()
        self._charges.update()
        self._extras.update()
        self._emails.update()
        self._forms.update()
        return self
    
    def delete(self) -> None:
        """
        Delete the booking record from the database.
        Deletes all components associated with this booking.
        
        Returns:
            None
        """
        if not self._details.id:
            return logerror('Cannot delete booking without a valid ID.')
        
        self._details.delete()
        self._arrival.delete()
        self._departure.delete()
        self._charges.delete()
        self._extras.delete()
        self._emails.delete()
        self._forms.delete()

    def exists(self) -> bool:
        """
        Check if this booking already exists in the database.
        First checks if the details ID is set, then performs a database query
        to find a matching booking based on arrival/departure dates and property.
        
        Returns:
            True if the booking exists in the database, False otherwise
            
        Raises:
            RuntimeError: If essential booking criteria are missing
        """
        if self._details.exists():
            return True
       
        if not self.arrival.date:
            return logerror('Not enough criteria specified. Failed on arrival date specification.')
       
        if not self.departure.date:
            return logerror('Not enough criteria specified. Failed on departure date specification.')
      
        conditionsString = 'SELECT bookings.id, bookings.guestId FROM bookings'
        conditionsString += ' JOIN arrivals ON arrivals.bookingId = bookings.id'
        conditionsString += ' JOIN departures ON departures.bookingId = bookings.id'
        conditionsString += f' WHERE arrivals.date = "{self._arrival.date}"'
        conditionsString += f' AND departures.date = "{self._departure.date}"'
        conditionsString += f' AND bookings.propertyId = "{self._details.propertyId}"'
        conditionsString += f' AND bookings.enquiryStatus = "{self._details.enquiryStatus}"'
        result = self._database.runSQL(conditionsString)._cursor.fetchone()
      
        if result:
            self._details.id = result[0]
            self._details.guestId = result[1]
            self._guest.id = result[1]
            return True
        
        return False

    def _set_booking_id(self, bookingId: int) -> 'Booking':
        """
        Set the booking ID on all component objects.
        
        Args:
            bookingId: The ID to set on all booking components
            
        Returns:
            Self for method chaining
        """
        self._arrival.bookingId = bookingId
        self._departure.bookingId = bookingId
        self._charges.bookingId = bookingId
        self._extras.bookingId = bookingId
        self._emails.bookingId = bookingId
        self._forms.bookingId = bookingId
        return self
    
    def __repr__(self) -> str:
        """
        Get a string representation of the booking suitable for debugging.
        
        Returns:
            A concise representation of the booking
        """
        string = ''
        if self._guest.hasValue('firstName'):
            string += f'{self._guest.firstName} '

        if self._guest.hasValue('lastName'):
            try:
                string += f'{self._guest.lastName.upper()}'
            except AttributeError:
                string += f'{self._guest.lastName}'

        if self._property.hasValue('shortName'):
            string += f' in {self._property.shortName}'

        elif self._property.hasValue('name'):
            string += f' in {self._property.name}'

        elif self._details.propertyName:
            string += f' in {self._details.propertyName}'

        elif self._details.hasValue('propertyId'):
            string += f' Prop-ID {self._details.propertyId}'

        if self._arrival.hasValue('date'):
            string += f' on {dates.euDate(self._arrival.date)}'

        if self._departure.hasValue('date'):
            string += f' until {dates.euDate(self._departure.date)}'

        if self._details.hasValue('enquirySource'):
            string += f' from {self._details.enquirySource}'

        if self._details.hasValue('id'):
            string += f' ID {self._details.id}'

        if self._details.hasValue('enquiryStatus'):
            string += f' - {self._details.enquiryStatus.upper()}'

        return string
    
    def __str__(self) -> str:
        """
        Get a detailed string representation of the booking with all components.
        
        Returns:
            A detailed representation of the booking showing all components
        """
        string = '\n\t\t_____BOOKING_____'
        string += self._details.__str__()
        string += self._guest.__str__()
        string += self._arrival.__str__()
        string += self._departure.__str__()
        string += self._charges.__str__()
        string += self._extras.__str__()
        string += self._emails.__str__()
        string += self._forms.__str__()
        string += self._property.__str__()
        return string