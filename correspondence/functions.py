from default.booking.booking import Booking
from default.database.database import Database
from default.database.functions import search_bookings
from default.dates import dates


def get_email_bookings(database: Database, bookingId: int | None = None, 
                      noBlocks: bool = True) -> Database:
    """
    Create a database search for email-related booking information.
    
    Sets up a search query with relevant fields selected for email operations,
    optionally filtering for a specific booking.
    
    Args:
        database: Database connection object.
        bookingId: Optional ID to filter for a specific booking.
        noBlocks: Whether to exclude blocked periods.
        
    Returns:
        Configured database search query object.
    """
    search = search_bookings(database, noBlocks=noBlocks)
    select = search.emails.select()
    select.id()
   
    select = search.properties.select()
    select.name()
    select.shortName()
    
    select = search.guests.select()
    select.firstName()
    select.lastName()
   
    if bookingId:
        where = search.details.where()
        where.id().isEqualTo(bookingId)
    return search


# Booking details functions

def determine_arrival_details(booking: Booking) -> str:
    """
    Determine the arrival details string for a booking.
    
    Creates a human-readable string with flight information or indicates
    when time information is missing.
    
    Args:
        booking: Booking object with arrival information.
        
    Returns:
        Formatted arrival details string.
    """
    if booking.arrival.flightNumber:
        if not booking.arrival.time:
            return booking.arrival.flightNumber + ' @ Unknown Time (*Please provide*)'
   
    return booking.arrival.prettyDetails


def determine_departure_details(booking: Booking) -> str:
    """
    Determine the departure details string for a booking.
    
    Creates a human-readable string with flight information or indicates
    when time information is missing.
    
    Args:
        booking: Booking object with departure information.
        
    Returns:
        Formatted departure details string.
    """
    if booking.departure.flightNumber:
        if not booking.departure.time:
            return booking.departure.flightNumber + ' @ Unknown Time (*Please provide*)'
    
    return booking.departure.prettyDetails


def determine_balance_payment(booking: Booking, orderForms: object = None, 
                             bookingId: int = None) -> str | None:
    """
    Determine the balance payment due for a booking.
    
    Calculates the payment amount based on booking currency, reservation total,
    and whether payment has already been made.
    
    Args:
        booking: Booking object with charge information.
        orderForms: Optional order forms object with payment information.
        bookingId: Optional booking ID for payment verification.
        
    Returns:
        Formatted payment amount with currency symbol or None if already paid.
    """
    booking.charges.applyExchangeRate = False
    if booking.charges.currency == 'GBP':
        symbol = '£'
    else:
        symbol = '€'
   
    if not orderForms:
        return symbol + '{:.2f}'.format(booking.charges.totalRental * .75)
   
    orderForms.goTo(booking.details.PIMSId)
   
    if not bookingId and 'payment of balance' in orderForms.completedTasks.lower():
        return None
   
    bookingDeposit = orderForms.bookingDeposit    
    return symbol + '{:.2f}'.format(booking.charges.totalRental - bookingDeposit)


def determine_balance_payment_date(booking: Booking) -> str:
    """
    Calculate the due date for the balance payment.
    
    Returns a formatted date string 56 days before arrival.
    
    Args:
        booking: Booking object with arrival information.
        
    Returns:
        Formatted date string for balance payment.
    """
    return dates.prettyDate(dates.calculate(booking.arrival.date, days=-56))


# Extra services functions

def determine_on_site_extras(extras: list[str]) -> list[str]:
    """
    Filter a list of extras to only include on-site services.
    
    Excludes airport transfers and extra nights from the list.
    
    Args:
        extras: List of all booking extras.
        
    Returns:
        List of on-site extras only.
    """
    return list(filter(_determine_neither_airport_nor_nights, extras))


def _determine_neither_airport_nor_nights(extra: str) -> bool:
    """
    Check if an extra is neither airport-related nor extra nights.
    
    Args:
        extra: The extra service description to check.
        
    Returns:
        True if the extra is not related to airport transfers or extra nights.
    """
    extra = extra.lower()
    return 'airport' not in extra and 'extra nights' not in extra


def determine_inbound_transfer(booking: Booking) -> bool:
    """
    Determine if the booking includes an inbound airport transfer.
    
    Args:
        booking: Booking object with extras information.
        
    Returns:
        True if the booking includes an inbound airport transfer.
    """
    return booking.extras.airportTransfers or booking.extras.airportTransferInboundOnly


def determine_outbound_transfer(booking: Booking) -> bool:
    """
    Determine if the booking includes an outbound airport transfer.
    
    Args:
        booking: Booking object with extras information.
        
    Returns:
        True if the booking includes an outbound airport transfer.
    """
    return booking.extras.airportTransfers or booking.extras.airportTransferOutboundOnly