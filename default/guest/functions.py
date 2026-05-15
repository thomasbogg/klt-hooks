from default.booking.booking import Booking
from default.database.functions import search_valid_bookings


def guest_has_stayed_before(booking: Booking) -> bool:
    """
    Check if a guest has stayed in any property before this booking.
    
    Parameters:
        booking: The booking object to check.
        
    Returns:
        bool: True if the guest has stayed before, False otherwise.
    """
    search = search_valid_bookings()
    where = search.details.where()
    where.guestId().isEqualTo(booking.details.guestId)

    where = search.departures.where()
    where.date().isLessThan(booking.arrival.date)

    results = search.fetchall()
    return bool(results)