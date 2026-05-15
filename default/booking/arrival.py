import datetime
from libraries.database.row import Row as DatabaseRow
from default.dates import dates


class Arrival(DatabaseRow):
    """
    Represents an arrival associated with a booking.
    
    This class handles arrival information including flight details,
    arrival time, and special arrangements like meet and greet.
    """
    
    def __init__(self, database: object = None) -> None:
        """
        Initialize an Arrival object.
        
        Args:
            database: The database connection to use
        """
        super().__init__(database, 'arrivals', foreignKeys=['bookingId'])
           
    @property
    def bookingId(self) -> int:
        """
        Get the booking ID associated with this arrival.
        
        Returns:
            The booking ID
        """
        return self._get('bookingId')

    @bookingId.setter
    def bookingId(self, value: int) -> None:
        """
        Set the booking ID for this arrival.
        
        Args:
            value: The booking ID to set
        """
        return self._set('bookingId', value)

    @property
    def date(self) -> datetime.date:
        """
        Get the arrival date.
        
        Returns:
            The arrival date object
        """
        return self._get('date')

    @date.setter
    def date(self, value: date) -> None:
        """
        Set the arrival date.
        
        Args:
            value: The date to set
        """
        return self._set('date', value)
    
    @property
    def prettyDate(self) -> str:
        """
        Get a formatted string representation of the arrival date.
        
        Returns:
            A formatted date string
        """
        return dates.prettyDate(self.date)

    @property
    def flightNumber(self) -> str:
        """
        Get the flight number for this arrival.
        
        Returns:
            The flight number
        """
        return self._get('flightNumber')

    @flightNumber.setter
    def flightNumber(self, value: str) -> None:
        """
        Set the flight number for this arrival.
        
        Args:
            value: The flight number to set
        """
        return self._set('flightNumber', value)

    @property
    def isFaro(self) -> bool:
        """
        Check if the arrival is at Faro airport.
        
        Returns:
            True if the arrival is at Faro airport, False otherwise
        """
        return self._get('isFaro')

    @isFaro.setter
    def isFaro(self, value: bool) -> None:
        """
        Set whether the arrival is at Faro airport.
        
        Args:
            value: True if arriving at Faro, False otherwise
        """
        return self._set('isFaro', value)

    @property
    def time(self) -> datetime.time:
        """
        Get the arrival time.
        
        Returns:
            The arrival time
        """
        return self._get('time')

    @time.setter
    def time(self, value: time) -> None:
        """
        Set the arrival time.
        
        Args:
            value: The arrival time to set
        """
        return self._set('time', value)

    @property
    def details(self) -> str:
        """
        Get additional details about the arrival.
        
        Returns:
            Arrival details
        """
        return self._get('details')

    @details.setter
    def details(self, value: str) -> None:
        """
        Set additional details about the arrival.
        
        Args:
            value: The details to set
        """
        return self._set('details', value)

    @property
    def selfCheckIn(self) -> bool | str:
        """
        Check if self check-in is enabled for this arrival.
        
        Returns:
            True if self check-in is enabled, False otherwise
        """
        return self._get('selfCheckIn')

    @selfCheckIn.setter
    def selfCheckIn(self, value: bool) -> None:
        """
        Set whether self check-in is enabled.
        
        Args:
            value: True to enable self check-in, False otherwise
        """
        return self._set('selfCheckIn', value)

    @property
    def meetGreet(self) -> bool:
        """
        Check if meet and greet service is requested for this arrival.
        
        Returns:
            True if meet and greet is requested, False otherwise
        """
        return self._get('meetGreet')

    @meetGreet.setter
    def meetGreet(self, value: bool) -> None:
        """
        Set whether meet and greet service is requested.
        
        Args:
            value: True to request meet and greet, False otherwise
        """
        return self._set('meetGreet', value)

    @property
    def manualDate(self) -> datetime.date:
        """
        Get the manually set date, if any.
        
        Returns:
            The manually set date
        """
        return self._get('manualDate')

    @manualDate.setter
    def manualDate(self, value: date) -> None:
        """
        Set a manual date for this arrival.
        
        Args:
            value: The manual date to set
        """
        return self._set('manualDate', value)
    
    @property
    def isSoon(self) -> bool:
        """
        Check if the arrival is happening soon (within 17 days).
        
        Returns:
            True if the arrival is soon, False otherwise
        """
        return dates.subtractDates(dates.date(), self.date) < 17
    
    @property
    def isToday(self) -> bool:
        """
        Check if the arrival is today.
        
        Returns:
            True if the arrival is today, False otherwise
        """
        return dates.date == self.date
    
    @property
    def isTomorrow(self) -> bool:
        """
        Check if the arrival is tomorrow.
        
        Returns:
            True if the arrival is tomorrow, False otherwise
        """
        return dates.date == dates.calculate(self.date, days=1)
    
    @property
    def isVerySoon(self) -> bool:
        """
        Check if the arrival is very soon (within 5 days).
        
        Returns:
            True if the arrival is very soon, False otherwise
        """
        return dates.subtractDates(dates.date(), self.date) < 5
    
    @property
    def isImminent(self) -> bool:
        """
        Check if the arrival is imminent (within 3 days).
        
        Returns:
            True if the arrival is imminent, False otherwise
        """
        return dates.subtractDates(dates.date(), self.date) < 3
    
    @property
    def isLate(self) -> bool | None:
        """
        Check if the arrival is late at night (after 22:50).
        
        Returns:
            True if the arrival is late, False if not, None if time is invalid
        """
        if not self._time_is_valid():
            return None
        return self.time > dates.time(22, 00)
    
    @property
    def isEarly(self) -> bool | None:
        """
        Check if the arrival is early in the morning (before 6:00).
        
        Returns:
            True if the arrival is early, False if not, None if time is invalid
        """
        if not self._time_is_valid():
            return None
        return self.time < dates.time(6, 0)
    
    @property
    def prettyTime(self) -> str:
        """
        Get a formatted string representation of the arrival time.
        
        Returns:
            A formatted time string
        """
        return dates.prettyTime(self.time)
    
    @property
    def timeIsValid(self) -> bool:
        """
        Check if the arrival time is valid.
        
        Returns:
            True if time is valid, False otherwise
        """
        return self._time_is_valid()
    
    @property
    def prettyDetails(self) -> str:
        """
        Get a formatted string with detailed arrival information.
        
        Returns:
            A formatted string with arrival details
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
            if 'ETA' in self.details or '@' in self.details:
                return self.details
            if self._time_is_valid():
                return f'{self.details} @ {self.prettyTime}'
        
        if not self.details and self._time_is_valid():
            return f'ETA @ {self.prettyTime}'
        
        return 'Unk. Arr. Details'
    
    @property
    def otherPrettyDetails(self) -> str | None:
        """
        Get additional formatted details if available.
        
        Returns:
            Additional formatted details or None if not available
        """
        if not self.flightNumber:
            return None
        if self.details:
            return self.details
    
    @property
    def meetGreetIsLate(self) -> bool | None:
        """
        Check if the arrival time is too late for meet and greet service.
        
        Returns:
            True if too late for meet and greet, False if not, None if time is invalid
        """
        if not self.flightNumber:
            if self._time_is_valid():
                return self.time > dates.time(20, 0)
        
        if self._time_is_valid():
            if not self.isFaro:
                return self.time > dates.time(15, 0)
            return self.time > dates.time(18, 0)
        return None
        
    @property
    def eta(self) -> datetime.time | None:
        """
        Calculate the estimated time of arrival at accommodation.
        
        Returns:
            The estimated arrival time or None if time is invalid
        """
        if not self.flightNumber:
            if self._time_is_valid():
                return self.time
            return None
        
        if self._time_is_valid():
            if self.isFaro:
                return dates.calculate(time=self.time, hours=1)
            return dates.calculate(time=self.time, hours=4)
        return None
    
    @property
    def year(self) -> int:
        """
        Get the year of the arrival date.
        
        Returns:
            The year
        """
        return self.date.year
    
    @property
    def month(self) -> int:
        """
        Get the month of the arrival date.
        
        Returns:
            The month (1-12)
        """
        return self.date.month
    
    @property
    def day(self) -> int:
        """
        Get the day of the arrival date.
        
        Returns:
            The day of the month
        """
        return self.date.day
    
    @property
    def weekday(self) -> int:
        """
        Get the weekday of the arrival date.
        
        Returns:
            The weekday (0-6, with Monday being 0)
        """
        return self.date.weekday()
    
    @property
    def hasDetails(self) -> bool:
        """
        Check if this arrival has any details provided.
        
        Returns:
            True if arrival has details, False otherwise
        """
        return self.details or self.timeIsValid or self.flightNumber
    
    def _time_is_valid(self) -> bool:
        """
        Check if the arrival time is valid.
        
        Returns:
            True if time is valid, False otherwise
        """
        return self.time and self.time > dates.time(0, 0)