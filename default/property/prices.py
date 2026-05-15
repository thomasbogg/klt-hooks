from typing import Any

from libraries.database.row import Row as DatabaseRow
from default.dates import dates


class Prices(DatabaseRow):
    """
    Represents monthly rental prices for a property.
    
    This class handles database operations for property prices, allowing
    retrieval and modification of nightly rates for each month of the year.
    """

    def __init__(self, database: Any | None = None) -> None:
        """
        Initialize a property prices object.
        
        Args:
            database: The database connection to use. If None, a default connection will be used.
        """
        super().__init__(database, 'propertyPrices')

    def month(self, month: str | int) -> float | None:
        """
        Get the price for a specific month by name.
        
        Args:
            monthName: The name of the month to get the price for.
            
        Returns:
            The price for the specified month or None if not set.
        """
        return self._get(self._get_database_month(month))
    
    def setMonth(self, month: str | int, price: float) -> None:
        """
        Set the price for a specific month.
        
        Args:
            month: The name or number of the month to set the price for.
            price: The price to set for the specified month.
        """
        self._set(self._get_database_month(month), price)

    @property
    def year(self) -> int:
        """
        Get the specific year of the price.
        
        Returns:
            The price for the specified year or None if not set.
        """
        return self._get("year")
    
    @year.setter
    def year(self, value: int) -> None:
        """
        Set the specific year of the prices.
        
        Args:
            value: The year to set the price for.
        """
        self._set('year', value)

    # Month-specific properties
    @property
    def january(self) -> float | None:
        """
        Get the January price.
        
        Returns:
            The price for January or None if not set.
        """
        return self._get('january')

    @january.setter
    def january(self, price: float) -> None:
        """
        Set the January price.
        
        Args:
            price: The price to set for January.
        """
        self._set('january', price)

    @property
    def february(self) -> float | None:
        """
        Get the February price.
        
        Returns:
            The price for February or None if not set.
        """
        return self._get('february')

    @february.setter
    def february(self, price: float) -> None:
        """
        Set the February price.
        
        Args:
            price: The price to set for February.
        """
        self._set('february', price)

    @property
    def march(self) -> float | None:
        """
        Get the March price.
        
        Returns:
            The price for March or None if not set.
        """
        return self._get('march')

    @march.setter
    def march(self, price: float) -> None:
        """
        Set the March price.
        
        Args:
            price: The price to set for March.
        """
        self._set('march', price)

    @property
    def april(self) -> float | None:
        """
        Get the April price.
        
        Returns:
            The price for April or None if not set.
        """
        return self._get('april')

    @april.setter
    def april(self, price: float) -> None:
        """
        Set the April price.
        
        Args:
            price: The price to set for April.
        """
        self._set('april', price)

    @property
    def may(self) -> float | None:
        """
        Get the May price.
        
        Returns:
            The price for May or None if not set.
        """
        return self._get('may')

    @may.setter
    def may(self, price: float) -> None:
        """
        Set the May price.
        
        Args:
            price: The price to set for May.
        """
        self._set('may', price)

    @property
    def june(self) -> float | None:
        """
        Get the June price.
        
        Returns:
            The price for June or None if not set.
        """
        return self._get('june')

    @june.setter
    def june(self, price: float) -> None:
        """
        Set the June price.
        
        Args:
            price: The price to set for June.
        """
        self._set('june', price)

    @property
    def july(self) -> float | None:
        """
        Get the July price.
        
        Returns:
            The price for July or None if not set.
        """
        return self._get('july')

    @july.setter
    def july(self, price: float) -> None:
        """
        Set the July price.
        
        Args:
            price: The price to set for July.
        """
        self._set('july', price)

    @property
    def august(self) -> float | None:
        """
        Get the August price.
        
        Returns:
            The price for August or None if not set.
        """
        return self._get('august')

    @august.setter
    def august(self, price: float) -> None:
        """
        Set the August price.
        
        Args:
            price: The price to set for August.
        """
        self._set('august', price)

    @property
    def september(self) -> float | None:
        """
        Get the September price.
        
        Returns:
            The price for September or None if not set.
        """
        return self._get('september')

    @september.setter
    def september(self, price: float) -> None:
        """
        Set the September price.
        
        Args:
            price: The price to set for September.
        """
        self._set('september', price)

    @property
    def october(self) -> float | None:
        """
        Get the October price.
        
        Returns:
            The price for October or None if not set.
        """
        return self._get('october')

    @october.setter
    def october(self, price: float) -> None:
        """
        Set the October price.
        
        Args:
            price: The price to set for October.
        """
        self._set('october', price)

    @property
    def november(self) -> float | None:
        """
        Get the November price.
        
        Returns:
            The price for November or None if not set.
        """
        return self._get('november')

    @november.setter
    def november(self, price: float) -> None:
        """
        Set the November price.
        
        Args:
            price: The price to set for November.
        """
        self._set('november', price)

    @property
    def december(self) -> float | None:
        """
        Get the December price.
        
        Returns:
            The price for December or None if not set.
        """
        return self._get('december')

    @december.setter
    def december(self, price: float) -> None:
        """
        Set the December price.
        
        Args:
            price: The price to set for December.
        """
        self._set('december', price)

    @property
    def festive(self) -> float | None:
        """
        Get the festive price.
        
        Returns:
            The festive price or None if not set.
        """
        return self._get('festive')
    
    @festive.setter
    def festive(self, price: float) -> None:
        """
        Set the festive price.
        
        Args:
            price: The price to set for the festive period.
        """
        self._set('festive', price)

    @property
    def earlyWinterMonthlyRate(self) -> float | None:
        """
        Get the early winter monthly rate.
        
        Returns:
            The early winter monthly rate or None if not set.
        """
        return self._get('earlyWinterMonthlyRate')
    
    @earlyWinterMonthlyRate.setter
    def earlyWinterMonthlyRate(self, price: float) -> None:
        """
        Set the early winter monthly rate.
        
        Args:
            price: The price to set for the early winter monthly rate.
        """
        self._set('earlyWinterMonthlyRate', price)

    @property
    def lateWinterMonthlyRate(self) -> float | None:
        """
        Get the late winter monthly rate.
        
        Returns:
            The late winter monthly rate or None if not set.
        """
        return self._get('lateWinterMonthlyRate')
    
    @lateWinterMonthlyRate.setter
    def lateWinterMonthlyRate(self, price: float) -> None:
        """
        Set the late winter monthly rate.
        
        Args:
            price: The price to set for the late winter monthly rate.
        """
        self._set('lateWinterMonthlyRate', price)

    def _get_database_month(self, month: int | str) -> int | None:
        """
        Get the database month for this price record.
        
        Returns:
            The database month or None if not set.
        """
        if isinstance(month, str):
            return month.lower()
        if month == 13:
            return 'festive'
        elif month == 14:
            return 'earlyWinterMonthlyRate'
        elif month == 15:
            return 'lateWinterMonthlyRate'
        return dates.prettyMonth(month).lower()

    def _get_condition(self) -> str:
        """
        Get the database condition to identify this price record.
        
        Returns:
            A SQL condition string based on the property identifier.
        """
        return f'name="{self._get("name")}" AND year={self._get("year")}'