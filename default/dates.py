import datetime

from libraries.dates import dates as _dates
from libraries.utils import logerror, logwarning


class dates(_dates):
    """
    Extended date utility class for KLT application.
    
    Extends the base Dates class with specialized functionality for
    handling dates and times in the context of property rentals and bookings.
    """

    def __init__(self) -> None:
        """Initialize a Dates instance."""
        super().__init__()

    @classmethod
    def isUpdateHour(cls) -> bool:
        """
        Check if the current hour is suitable for updates.
        
        Returns:
            True if the current hour is after 5 PM or before 10 AM.
        """
        return 16 < cls.hour() or cls.hour() < 10

    @classmethod
    def isHighSeason(cls, date: datetime.date) -> bool:
        """
        Check if a given date falls within the high season (April through October).
        
        Args:
            date: The date to check.
            
        Returns:
            True if the date is in high season.
        """
        return 3 < date.month < 11

    @classmethod
    def isNewVATRegime(cls, date: datetime.date) -> bool:
        """
        Check if a given date is after the new VAT law for foreign citizens (1 July 2025).
        
        Args:
            date: The date to check.
            
        Returns:
            True if the date is after the start of the new law.
        """
        return date >= cls.date(2025, 7, 1)
    
    @classmethod
    def arrivalIsSoon(cls, date: datetime.date) -> bool:
        """
        Check if an arrival date is less than 17 days away.
        
        Args:
            date: The arrival date to check.
            
        Returns:
            True if the arrival is within 17 days.
        """
        if (date - cls.date()).days < 17: 
            return True
        return False
    
    @classmethod
    def arrivalIsVerySoon(cls, date: datetime.date) -> bool:
        """
        Check if an arrival date is less than 5 days away.
        
        Args:
            date: The arrival date to check.
            
        Returns:
            True if the arrival is within 5 days.
        """
        if (date - cls.date()).days < 5: 
            return True
        return False

    @classmethod
    def breakDatesByYears(cls, 
                         start: datetime.date, 
                         end: datetime.date) -> list[tuple[datetime.date, datetime.date]]:
        """
        Break a date range into year-based chunks.
        
        Args:
            start: The start date of the range.
            end: The end date of the range.
            
        Returns:
            A list of tuples containing (start_date, end_date) for each year.
        """
        if start.year == end.year: 
            return [(start, end)]
        
        dates = []
        for year in range(start.year, end.year + 1):
            if start.year == year: 
                dates.append((start, cls.date(year, 12, 31)))
            elif year == end.year: 
                return dates + [(cls.date(year, 1, 1), end)]
            else: 
                dates.append((cls.date(year, 1, 1), cls.date(year, 12, 31)))    
        return dates

    @classmethod
    def breakDatesByMonths(cls, 
                          start: datetime.date, 
                          end: datetime.date) -> list[tuple[datetime.date, datetime.date]]:
        """
        Break a date range into month-based chunks.
        
        Args:
            start: The start date of the range.
            end: The end date of the range.
            
        Returns:
            A list of tuples containing (start_date, end_date) for each month.
        """
        if start.year == end.year and start.month == end.month:
            return [(start, end)]
        
        dates = []
        for year in range(start.year, end.year + 1):
            for month in range(1, 13):
                if year == start.year and month < start.month: 
                    continue
                daysInMonth = cls.daysInMonth(year, month)
                if year == start.year and month == start.month: 
                    dates.append((start, cls.date(year, month, daysInMonth)))
                elif year == end.year and month == end.month: 
                    dates.append((cls.date(year, month, 1), end))
                    return dates
                else: 
                    dates.append((cls.date(year, month, 1), cls.date(year, month, daysInMonth)))
        return dates
    
    @classmethod
    def convertToTime(cls, string: str) -> datetime.time | None:
        """
        Convert a string representation to a time object.
        
        Handles various time formats like '14:30', '14.30', '14h30', etc.
        
        Args:
            string: The string time representation to convert.
            
        Returns:
            A time object if conversion successful, or None if conversion failed.
        """
        string = string.strip()
        if len(string) > 5: 
            return logerror(f'Cannot convert given time string with confidence: {string}')
        
        broken = None
        for separator in ['.', ':', ';', 'H', 'h']:
            if separator in string:
                broken = string.split(separator)
                break
                
        if broken:
            return cls.time(hour=int(broken[0]), minute=int(broken[1]))
            
        logwarning(f'Cannot find separator in time string: {string}. Will try to convert anyway.')
        if len(string) == 4: 
            return cls.time(hour=int(string[:2]), minute=int(string[2:]))
        if len(string) == 3:
            return cls.time(hour=int(string[0]), minute=int(string[1:]))
        
        return None

    @classmethod
    def daysperMonth(cls, start: datetime.date, end: datetime.date) -> dict[int: dict[int:int]]:
        """
        Calculate the number of booked days per month between two dates.
        
        For a given date range, computes how many days fall within each month,
        returning a list of (year, month, days) tuples.
        
        Args:
            start: The start date of the range.
            end: The end date of the range.
            
        Returns:
            A list of tuples containing (year, month, days) for each month
            in the date range.
        """
        if start.year == end.year and start.month == end.month:
            return {start.year: {start.month: end.day - start.day + 1}}
        result = {}
        for year in range(start.year, end.year + 1):
            for month in range(1, 13):
                if year == start.year and month < start.month:
                    continue
                daysInMonth = cls.daysInMonth(year, month)
                
                if year == start.year and month == start.month:
                    result[year] = {month: daysInMonth - start.day + 1}
                elif year == end.year and month == end.month:
                    result[year] = {month: end.day}
                    return result
                else:
                    result[year] = {month: daysInMonth}

        return result