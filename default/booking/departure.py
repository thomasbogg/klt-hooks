import datetime

from libraries.database.row import Row as DatabaseRow
from default.dates import dates


class Departure(DatabaseRow):
    """
    Represents departure information for a booking.
    Tracks details like departure date, flight number, time, and departure location.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Departure instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'departures', foreignKeys=['bookingId'])
    
    # Basic properties
    @property
    def bookingId(self) -> int | None:
        """
        Get the booking ID.
        
        Returns:
            The ID of the associated booking
        """
        return self._get('bookingId')

    @bookingId.setter
    def bookingId(self, value: int) -> None:
        """
        Set the booking ID.
        
        Args:
            value: The booking ID to set
        """
        self._set('bookingId', value)

    @property
    def date(self) -> datetime.date | None:
        """
        Get the departure date.
        
        Returns:
            The date of departure
        """
        return self._get('date')

    @date.setter
    def date(self, value: date) -> None:
        """
        Set the departure date.
        
        Args:
            value: The departure date to set
        """
        self._set('date', value)

    @property
    def time(self) -> datetime.time | None:
        """
        Get the departure time.
        
        Returns:
            The scheduled time of departure
        """
        return self._get('time')

    @time.setter
    def time(self, value: time) -> None:
        """
        Set the departure time.
        
        Args:
            value: The departure time to set
        """
        self._set('time', value)

    # Flight details
    @property
    def flightNumber(self) -> str | None:
        """
        Get the departure flight number.
        
        Returns:
            The flight number
        """
        return self._get('flightNumber')

    @flightNumber.setter
    def flightNumber(self, value: str) -> None:
        """
        Set the departure flight number.
        
        Args:
            value: The flight number to set
        """
        self._set('flightNumber', value)

    @property
    def isFaro(self) -> bool | None:
        """
        Get whether the departure is from Faro airport.
        
        Returns:
            True if departing from Faro, False if from another airport (e.g., Lisbon)
        """
        return self._get('isFaro')

    @isFaro.setter
    def isFaro(self, value: bool) -> None:
        """
        Set whether the departure is from Faro airport.
        
        Args:
            value: True if departing from Faro, False otherwise
        """
        self._set('isFaro', value)

    @property
    def details(self) -> str | None:
        """
        Get additional departure details.
        
        Returns:
            Additional details about the departure
        """
        return self._get('details')

    @details.setter
    def details(self, value: str) -> None:
        """
        Set additional departure details.
        
        Args:
            value: Additional departure details to set
        """
        self._set('details', value)

    # Additional properties
    @property
    def clean(self) -> bool | None:
        """
        Get whether cleaning is required after departure.
        
        Returns:
            True if cleaning is required, False otherwise
        """
        return self._get('clean')

    @clean.setter
    def clean(self, value: bool) -> None:
        """
        Set whether cleaning is required after departure.
        
        Args:
            value: True if cleaning is required, False otherwise
        """
        self._set('clean', value)

    @property
    def manualDate(self) -> bool | None:
        """
        Get whether the departure date was manually entered.
        
        Returns:
            True if date was manually entered, False otherwise
        """
        return self._get('manualDate')

    @manualDate.setter
    def manualDate(self, value: bool) -> None:
        """
        Set whether the departure date was manually entered.
        
        Args:
            value: True if date was manually entered, False otherwise
        """
        self._set('manualDate', value)
    
    # Calculated properties
    @property
    def prettyDate(self) -> str | None:
        """
        Get a formatted string representation of the departure date.
        
        Returns:
            Formatted departure date string or None if date is not set
        """
        return dates.prettyDate(self.date)
    
    @property
    def prettyTime(self) -> str | None:
        """
        Get a formatted string representation of the departure time.
        
        Returns:
            Formatted departure time string or None if time is not set
        """
        return dates.prettyTime(self.time)
    
    @property
    def timeIsValid(self) -> bool:
        """
        Check if the departure time is valid.
        
        Returns:
            True if the time is set and greater than midnight, False otherwise
        """
        return self._time_is_valid()
    
    @property
    def prettyDetails(self) -> str:
        """
        Get a formatted string with the departure details.
        
        Returns:
            A human-readable string combining flight number, time, and location information
        """
        if self.flightNumber:
            string = self.flightNumber
        
            if self._time_is_valid():
                string += ' - ' + self.prettyTime
            else:
                string += ' @ Unk. Time'
        
            if not self.isFaro:
                string += ' (LISBON)'
            return string
        
        if self.details:
            if 'ETD' in self.details or '@' in self.details:
                return self.details
            
            if self._time_is_valid():
                return f'{self.details} @ {self.prettyTime}'
            
        if not self.details and self._time_is_valid():
            return f'ETD @ {self.prettyTime}'

        return 'Unk. Dep. Details'
    
    @property
    def etd(self) -> datetime.time | None:
        """
        Calculate the Estimated Time of Departure based on flight and airport.
        For Faro departures, ETD is 3 hours before flight time.
        For other airports, ETD is 6 hours before flight time.
        
        Returns:
            Calculated departure time or None if time is not valid
        """
        if not self.flightNumber:
            if self._time_is_valid():
                return self.time
            return None
      
        if self._time_is_valid():
            if self.isFaro:
                return dates.calculate(time=self.time, hours=-3)
            return dates.calculate(time=self.time, hours=-6)
        return None

    # Date component properties
    @property
    def year(self) -> int | None:
        """
        Get the year of the departure date.
        
        Returns:
            The year component of the departure date or None if date is not set
        """
        return self.date.year if self.date else None
    
    @property
    def month(self) -> int | None:
        """
        Get the month of the departure date.
        
        Returns:
            The month component of the departure date or None if date is not set
        """
        return self.date.month if self.date else None
    
    @property
    def day(self) -> int | None:
        """
        Get the day of the departure date.
        
        Returns:
            The day component of the departure date or None if date is not set
        """
        return self.date.day if self.date else None
    
    @property
    def weekday(self) -> int | None:
        """
        Get the weekday of the departure date.
        
        Returns:
            The weekday of the departure date (0-6, where 0 is Monday) or None if date is not set
        """
        return self.date.weekday() if self.date else None
    
    def _time_is_valid(self) -> bool:
        """
        Check if the time is valid (exists and is after midnight).
        
        Returns:
            True if time is valid, False otherwise
        """
        return self.time is not None and self.time > dates.time(0, 0)