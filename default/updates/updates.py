from typing import Any

from libraries.database.row import Row as DatabaseRow
from default.dates import dates


class Update(DatabaseRow):
    """
    Represents a booking update entry in the database.
    
    This class handles database operations for tracking changes to bookings,
    including detail changes, extras changes, and booking cancellations.
    """
    
    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize an update record.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'updates', foreignKeys=['bookingId'])
           
    # Booking reference properties
    @property
    def bookingId(self) -> int | None:
        """
        Get the associated booking ID.
        
        Returns:
            The booking ID or None if not set.
        """
        return self._get('bookingId')

    @bookingId.setter
    def bookingId(self, value: int) -> None:
        """
        Set the associated booking ID.
        
        Args:
            value: The booking ID to set.
        """
        self._set('bookingId', value)

    # Date properties
    @property
    def date(self) -> str | None:
        """
        Get the date of the update.
        
        Returns:
            The update date or None if not set.
        """
        return self._get('date')

    @date.setter
    def date(self, value: str) -> None:
        """
        Set the date of the update.
        
        Args:
            value: The update date to set.
        """
        self._set('date', value)
    
    @property
    def prettyDate(self) -> str:
        """
        Get a formatted version of the update date.
        
        Returns:
            A human-readable formatted date string.
        """
        return dates.prettyDate(self.date)
    
    # Update content properties
    @property
    def details(self) -> str | None:
        """
        Get the booking detail changes.
        
        Returns:
            The details of changes or None if not set.
        """
        return self._get('details')
    
    @details.setter
    def details(self, value: str | None) -> None:
        """
        Set the booking detail changes.
        
        Args:
            value: The details of changes to set.
        """
        self._set('details', value)
    
    @property
    def extras(self) -> str | None:
        """
        Get the booking extras changes.
        
        Returns:
            The extras changes or None if not set.
        """
        return self._get('extras')
    
    @extras.setter
    def extras(self, value: str | None) -> None:
        """
        Set the booking extras changes.
        
        Args:
            value: The extras changes to set.
        """
        self._set('extras', value)

    @property
    def messages(self) -> str | None:
        """
        Get the booking messages changes.
        
        Returns:
            The messages changes or None if not set.
        """
        return self._get('messages')
    
    @messages.setter
    def messages(self, value: str | None) -> None:
        """
        Set the booking messages changes.
        
        Args:
            value: The messages changes to set.
        """
        self._set('messages', value)
    
    # Notification properties
    @property
    def emailSent(self) -> bool | None:
        """
        Get whether an email notification about this update was sent.
        
        Returns:
            Boolean indicating if email was sent, or None if not set.
        """
        return self._get('emailSent')
    
    @emailSent.setter
    def emailSent(self, value: bool) -> None:
        """
        Set whether an email notification about this update was sent.
        
        Args:
            value: Boolean indicating if email was sent.
        """
        self._set('emailSent', value)
    
    # Update type properties
    @property
    def isCancelledBooking(self) -> bool:
        """
        Check if this update represents a cancelled booking.
        
        Returns:
            True if this update is for a cancelled booking, False otherwise.
        """
        if not self.details:
            return False
        return 'cancelled booking' in self.details.lower()
    
    @property
    def isUpdatedBooking(self) -> bool:
        """
        Check if this update represents a booking detail change (not cancellation).
        
        Returns:
            True if this update is for a booking detail change, False otherwise.
        """
        return bool(self.details and not self.isCancelledBooking)
    
    @property
    def isCancelledTransfer(self) -> bool:
        """
        Check if this update represents a cancelled airport transfer.
        
        Returns:
            True if this update is for a cancelled airport transfer, False otherwise.
        """
        if not self.extras:
            return False
        return 'cancelled airport transfer' in self.extras.lower()
    
    def exists(self) -> bool:
        """
        Check if this update already exists in the database.
        
        Returns:
            True if an update with the same booking ID, date, and messages exists, False otherwise.
        """
        try:
            if self.id:
                return True
        except Exception:
            pass

        self.database.runSQL(f"SELECT id FROM updates WHERE bookingId = {self.bookingId} AND date = '{self.date}' AND messages = '{self.messages}'")
        if self.database._cursor.fetchone():
            return True
        return False