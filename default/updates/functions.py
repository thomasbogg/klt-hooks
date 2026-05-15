from default.booking.booking import Booking
from default.database.database import Database
from default.database.functions import get_booking, get_database
from default.dates import dates
from default.settings import VALID_BOOKING_STATUSES
from default.updates.updates import Update


def get_checkpoint_booking(database: Database, bookingId: int | None = None) -> Booking | None:
    """
    Retrieves a booking for checkpoint with specified conditions.
    
    Args:
        database: The database connection object.
        bookingId: The specific booking ID to filter by.
        
    Returns:
        A Booking object that matches the criteria or None if not found.
    """
    # Initialize search using valid bookings
    search = get_booking(database, id=bookingId)
    
    # Select details from the bookings table
    select = search.details.select()
    select.enquiryStatus()
    select.adults()
    select.children()
    select.babies()
    
    # Select arrival and departure dates
    select = search.arrivals.select()
    select.date()
    select.time()
    select.flightNumber()
    select.meetGreet()
    
    # Select departure details
    select = search.departures.select()
    select.date()
    select.time()
    select.flightNumber()
    select.clean()
    
    # Select property details
    select = search.properties.select()
    select.name()
    select.weClean()
    
    # Select extras (all columns)
    select = search.extras.select()
    select.all()
    
    # Select charges
    select = search.charges.select()
    select.basicRental()
    select.admin()
    select.security()
    select.securityMethod()
    select.platformFee()
    select.extraNights()
    select.currency()

    # Select emails
    select = search.emails.select()
    select.management()

    return search.fetchone()


def check_booking_updates(existingBooking: Booking, updatedBooking: Booking) -> None:
    """
    Check for changes between existing and updated booking and create update records.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information to compare against.
        
    Returns:
        None
    """
    if is_cancelled_booking(existingBooking, updatedBooking): 
        return None
    if property_has_changed(existingBooking, updatedBooking): 
        return None
    if arrival_date_has_changed(existingBooking, updatedBooking): 
        return None
    if departure_date_has_changed(existingBooking, updatedBooking): 
        return None
    if arrival_flight_has_changed(existingBooking, updatedBooking): 
        return None 
    if departure_flight_has_changed(existingBooking, updatedBooking): 
        return None 
    if arrival_time_has_changed(existingBooking, updatedBooking): 
        return None 
    if departure_time_has_changed(existingBooking, updatedBooking): 
        return None 
    if guest_numbers_have_changed(existingBooking, updatedBooking): 
        return None 
    if clean_has_changed(existingBooking, updatedBooking): 
        return None 
    #if meet_greet_has_changed(existingBooking, updatedBooking): 
    #    return None 

    airport_transfers_changes(existingBooking, updatedBooking)
    late_checkout_changes(existingBooking, updatedBooking)
    cot_changes(existingBooking, updatedBooking)
    high_chair_changes(existingBooking, updatedBooking)
    mid_stay_clean_changes(existingBooking, updatedBooking)
    other_request_changes(existingBooking, updatedBooking)
    if welcome_pack_changes(existingBooking, updatedBooking):
        welcome_pack_modifications_changes(existingBooking, updatedBooking)
    
    return None


# Helper functions
def has_transfers(existingBooking: Booking) -> bool:
    """
    Check if the booking includes any type of airport transfers.
    
    Args:
        existingBooking: The booking to check for transfers.
        
    Returns:
        True if any type of transfer is booked, False otherwise.
    """
    extras = existingBooking.extras
    if extras.airportTransfers: 
        return True
    if extras.airportTransferInboundOnly: 
        return True
    if extras.airportTransferOutboundOnly: 
        return True
    return False


def update_to_database(booking: Booking, details: str | None = None, extras: str | None = None, messages: str | None = None) -> bool:
    """
    Create an update record in the database for a booking.
    
    Args:
        booking: The booking to create an update for.
        details: Details about the update (for booking detail changes).
        extras: Details about the update (for extras changes).
        messages: Details about the update (for messages changes).
        
    Returns:
        True if the update was successful.
    """
    database = get_database()
   
    update = Update(database)
    update.date = dates.date()
    update.bookingId = booking.id
    update.details = details
    update.extras = extras
    update.messages = messages
    
    if not update.exists():
        update.insert()

    database.close()
    return True


# Booking status change functions
def is_cancelled_booking(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if a booking has been cancelled and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the booking was cancelled and update recorded, False otherwise.
    """
    if existingBooking.details.enquiryStatus in VALID_BOOKING_STATUSES:
        if updatedBooking.details.enquiryStatus not in VALID_BOOKING_STATUSES:
            return update_to_database(existingBooking, details='CANCELLED BOOKING')
    return False


# Property change functions
def property_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the property has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the property changed and update recorded, False otherwise.
    """
    if existingBooking.property.name != updatedBooking.details.propertyName:
        update = f'UPDATED BOOKING:Property has changed from {existingBooking.property.name}'
        return update_to_database(existingBooking, details=update)
    return False


# Date and time change functions
def arrival_date_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the arrival date has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the arrival date changed and update recorded, False otherwise.
    """
    if existingBooking.arrival.date != updatedBooking.arrival.date:
        update = f'UPDATED BOOKING:Arrival Date has changed from {existingBooking.arrival.prettyDate}'
        return update_to_database(existingBooking, details=update)
    return False 


def departure_date_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the departure date has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the departure date changed and update recorded, False otherwise.
    """
    if existingBooking.departure.date != updatedBooking.departure.date:
        update = f'UPDATED BOOKING:Departure Date has changed from {existingBooking.departure.prettyDate}'
        return update_to_database(existingBooking, details=update)
    return False


def arrival_flight_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the arrival flight details have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the arrival flight changed and update recorded, False otherwise.
    """
    if not updatedBooking.arrival.flightNumber:
        return False
    
    update = None
    if existingBooking.arrival.flightNumber != updatedBooking.arrival.flightNumber:
        update = f'UPDATED BOOKING:Arrival Flight Number has changed'

    if existingBooking.arrival.flightNumber:
        if existingBooking.arrival.time != updatedBooking.arrival.time:
            update = f'UPDATED BOOKING:Arrival Flight Time has changed'

    if update:
        return update_to_database(existingBooking, details=update)
    return False 


def departure_flight_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the departure flight details have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the departure flight changed and update recorded, False otherwise.
    """
    if not updatedBooking.departure.flightNumber:
        return False
    
    update = None
    if existingBooking.departure.flightNumber != updatedBooking.departure.flightNumber:
        update = f'UPDATED BOOKING:Departure Flight Number has changed'
    
    if existingBooking.departure.flightNumber:
        if existingBooking.departure.time != updatedBooking.departure.time:
            update = f'UPDATED BOOKING:Departure Flight Time has changed'

    if update:
        return update_to_database(existingBooking, details=update)
    return False


def arrival_time_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the arrival time has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the arrival time changed and update recorded, False otherwise.
    """
    if existingBooking.arrival.time != updatedBooking.arrival.time:
        update = f'UPDATED BOOKING:Arrival Time has changed from {existingBooking.arrival.prettyTime}'
        return update_to_database(existingBooking, details=update)
    return False


def departure_time_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the departure time has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the departure time changed and update recorded, False otherwise.
    """
    if existingBooking.departure.time != updatedBooking.departure.time:
        update = f'UPDATED BOOKING:Departure Time has changed from {existingBooking.departure.prettyTime}'
        return update_to_database(existingBooking, details=update)
    return False


# Guest and services change functions
def guest_numbers_have_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the number of guests has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the guest count changed and update recorded, False otherwise.
    """
    if existingBooking.details.totalGuests != updatedBooking.details.totalGuests:
        update = f'UPDATED BOOKING:Number of Guests has changed from {existingBooking.details.totalGuests}'
        return update_to_database(existingBooking, details=update)
    return False    


def clean_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the cleaning requirement has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the cleaning requirement changed and update recorded, False otherwise.
    """
    if existingBooking.departure.clean != updatedBooking.departure.clean:
        update = f'UPDATED BOOKING:Clean has changed from {yes_no(existingBooking.departure.clean)}'
        return update_to_database(existingBooking, details=update)
    return False


def meet_greet_has_changed(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if the meet & greet requirement has changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if the meet & greet changed and update recorded, False otherwise.
    """
    if existingBooking.property.weClean:
        return False
   
    if existingBooking.arrival.meetGreet != updatedBooking.arrival.meetGreet:
        update = f'UPDATED BOOKING:Meet & Greet has changed from {yes_no(existingBooking.arrival.meetGreet)}'
        return update_to_database(existingBooking, details=update)
    return False


# Extra services change functions
def airport_transfers_changes(existingBooking: Booking, updatedBooking: Booking, toDatabase: bool = True) -> bool:
    """
    Check if airport transfer requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if transfers changed and update recorded, False otherwise.
    """
    if (
        existingBooking.extras.airportTransfers and not
        updatedBooking.extras.airportTransfers
    ):
        if toDatabase:
            return update_to_database(existingBooking, extras='CANCELLED AIRPORT TRANSFERS')
        return True
    elif (
        not existingBooking.extras.airportTransfers and 
        updatedBooking.extras.airportTransfers
    ):
        return True
    elif (
        existingBooking.extras.airportTransferInboundOnly and not 
        updatedBooking.extras.airportTransferInboundOnly
    ):
        if toDatabase:
            return update_to_database(existingBooking, extras='CANCELLED AIRPORT TRANSFER INBOUND ONLY')
        return True
    elif (
        not existingBooking.extras.airportTransferInboundOnly and 
        updatedBooking.extras.airportTransferInboundOnly
    ):
        return True
    elif (
        existingBooking.extras.airportTransferOutboundOnly and not 
        updatedBooking.extras.airportTransferOutboundOnly
    ):
        if toDatabase:
            return update_to_database(existingBooking, extras='CANCELLED AIRPORT TRANSFER OUTBOUND ONLY')
        return True
    return False
    

def child_seats_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if child seat requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if child seat requirements changed and update recorded, False otherwise.
    """
    if existingBooking.extras.childSeats != updatedBooking.extras.childSeats:
        update = f'Child Seats have changed from {existingBooking.extras.childSeats}'
        return update_to_database(existingBooking, extras=update)
    return False


def excess_baggage_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if excess baggage requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if excess baggage changed and update recorded, False otherwise.
    """
    if existingBooking.extras.excessBaggage != updatedBooking.extras.excessBaggage:
        update = f'Excess Baggage has changed from {existingBooking.extras.excessBaggage}'
        return update_to_database(existingBooking, extras=update)
    return False    


def welcome_pack_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if welcome pack requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if welcome pack changed and update recorded, False otherwise.
    """
    if existingBooking.extras.welcomePack != updatedBooking.extras.welcomePack:
        update = f'Welcome Pack has been {added_cancelled(updatedBooking.extras.welcomePack)}'
        return update_to_database(existingBooking, extras=update)
    return False    
    

def welcome_pack_modifications_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if welcome pack modifications have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if welcome pack modifications changed and update recorded, False otherwise.
    """
    if existingBooking.extras.welcomePackModifications != updatedBooking.extras.welcomePackModifications:
        update = f'Welcome Pack Modifications have changed to {updatedBooking.extras.welcomePackModifications}'
        return update_to_database(existingBooking, extras=update)
    return False
    

def late_checkout_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if late checkout requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if late checkout changed and update recorded, False otherwise.
    """
    if existingBooking.extras.lateCheckout != updatedBooking.extras.lateCheckout:
        update = f'Late Checkout has been {added_cancelled(updatedBooking.extras.lateCheckout)}'
        return update_to_database(existingBooking, extras=update)
    return False


def cot_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if cot requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if cot requirements changed and update recorded, False otherwise.
    """
    if existingBooking.extras.cot != updatedBooking.extras.cot:
        update = f'Cot has been {added_cancelled(updatedBooking.extras.cot)}'
        return update_to_database(existingBooking, extras=update)
    return False


def high_chair_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if high chair requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if high chair requirements changed and update recorded, False otherwise.
    """
    if existingBooking.extras.highChair != updatedBooking.extras.highChair:
        update = f'High Chair has been {added_cancelled(updatedBooking.extras.highChair)}'
        return update_to_database(existingBooking, extras=update)
    return False


def mid_stay_clean_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if mid-stay clean requirements have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if mid-stay clean requirements changed and update recorded, False otherwise.
    """
    if existingBooking.extras.midStayClean != updatedBooking.extras.midStayClean:
        update = f'Mid-stay Clean has been {added_cancelled(updatedBooking.extras.midStayClean)}'
        return update_to_database(existingBooking, extras=update)
    return False


def other_request_changes(existingBooking: Booking, updatedBooking: Booking) -> bool:
    """
    Check if other requests have changed and record the update.
    
    Args:
        existingBooking: The current booking in the database.
        updatedBooking: The updated booking information.
        
    Returns:
        True if other requests changed and update recorded, False otherwise.
    """
    if existingBooking.extras.otherRequests != updatedBooking.extras.otherRequests:
        otherRequestsUpdate = updatedBooking.extras.otherRequests
        if otherRequestsUpdate:
            otherRequestsUpdate = otherRequestsUpdate.replace(' //', ',')
        update = f'Other Requests have changed to {otherRequestsUpdate}'
        return update_to_database(existingBooking, extras=update)
    return False    


# Helper formatting functions
def yes_no(boolean: bool) -> str:
    """
    Convert a boolean value to a YES/NO string.
    
    Args:
        boolean: The boolean value to convert.
        
    Returns:
        "YES" if True, "NO" if False.
    """
    return 'YES' if boolean else 'NO'


def added_cancelled(boolean: bool) -> str:
    """
    Convert a boolean value to an ADDED/CANCELLED string.
    
    Args:
        boolean: The boolean value to convert.
        
    Returns:
        "ADDED" if True, "CANCELLED" if False.
    """
    return 'ADDED' if boolean else 'CANCELLED'