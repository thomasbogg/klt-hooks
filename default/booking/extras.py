from libraries.database.row import Row as DatabaseRow


class Extras(DatabaseRow):
    """
    Represents additional services and amenities requested for a booking.
    
    This class tracks various extras that guests may request such as baby equipment,
    welcome packs, airport transfers, and special services during their stay.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Extras instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'extras', foreignKeys=['bookingId'])
    
    # Booking identification
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

    # Baby equipment
    @property
    def cot(self) -> bool | None:
        """
        Check if a baby cot has been requested.
        
        Returns:
            True if a cot has been requested, False otherwise
        """
        return self._get('cot')
    
    @cot.setter
    def cot(self, value: bool) -> None:
        """
        Set whether a baby cot has been requested.
        
        Args:
            value: True if a cot has been requested
        """
        self._set('cot', value)

    @property
    def highChair(self) -> bool | None:
        """
        Check if a high chair has been requested.
        
        Returns:
            True if a high chair has been requested, False otherwise
        """
        return self._get('highChair')
    
    @highChair.setter
    def highChair(self, value: bool) -> None:
        """
        Set whether a high chair has been requested.
        
        Args:
            value: True if a high chair has been requested
        """
        self._set('highChair', value)

    # Arrival and stay extras
    @property
    def welcomePack(self) -> bool | None:
        """
        Check if a welcome pack has been requested.
        
        Returns:
            True if a welcome pack has been requested, False otherwise
        """
        return self._get('welcomePack')
    
    @welcomePack.setter
    def welcomePack(self, value: bool) -> None:
        """
        Set whether a welcome pack has been requested.
        
        Args:
            value: True if a welcome pack has been requested
        """
        self._set('welcomePack', value)

    @property
    def welcomePackModifications(self) -> str | None:
        """
        Get any custom modifications to the welcome pack.
        
        Returns:
            Description of welcome pack modifications
        """
        return self._get('welcomePackModifications')
    
    @welcomePackModifications.setter
    def welcomePackModifications(self, value: str | None) -> None:
        """
        Set custom modifications to the welcome pack.
        
        Args:
            value: Description of welcome pack modifications
        """
        self._set('welcomePackModifications', value)

    @property
    def midStayClean(self) -> bool | None:
        """
        Check if a mid-stay cleaning has been requested.
        
        Returns:
            True if a mid-stay cleaning has been requested, False otherwise
        """
        return self._get('midStayClean')
    
    @midStayClean.setter
    def midStayClean(self, value: bool) -> None:
        """
        Set whether a mid-stay cleaning has been requested.
        
        Args:
            value: True if a mid-stay cleaning has been requested
        """
        self._set('midStayClean', value)

    # Departure extras
    @property
    def lateCheckout(self) -> bool | None:
        """
        Check if a late checkout has been requested.
        
        Returns:
            True if a late checkout has been requested, False otherwise
        """
        return self._get('lateCheckout')
    
    @lateCheckout.setter
    def lateCheckout(self, value: bool) -> None:
        """
        Set whether a late checkout has been requested.
        
        Args:
            value: True if a late checkout has been requested
        """
        self._set('lateCheckout', value)

    # Additional requests
    @property
    def otherRequests(self) -> str | None:
        """
        Get any other special requests made by the guest.
        
        Returns:
            Description of other requests
        """
        return self._get('otherRequests')
    
    @otherRequests.setter
    def otherRequests(self, value: str | None) -> None:
        """
        Set any other special requests made by the guest.
        
        Args:
            value: Description of other requests
        """
        self._set('otherRequests', value)

    @property
    def extraNights(self) -> bool | None:
        """
        Check if extra nights have been requested.
        
        Returns:
            True if extra nights have been requested, False otherwise
        """
        return self._get('extraNights')
    
    @extraNights.setter
    def extraNights(self, value: bool) -> None:
        """
        Set whether extra nights have been requested.
        
        Args:
            value: True if extra nights have been requested
        """
        self._set('extraNights', value)

    # Transportation
    @property
    def airportTransfers(self) -> bool | None:
        """
        Check if airport transfers (both ways) have been requested.
        
        Returns:
            True if airport transfers have been requested, False otherwise
        """
        return self._get('airportTransfers')
    
    @airportTransfers.setter
    def airportTransfers(self, value: bool) -> None:
        """
        Set whether airport transfers (both ways) have been requested.
        
        Args:
            value: True if airport transfers have been requested
        """
        self._set('airportTransfers', value)

    @property
    def airportTransferInboundOnly(self) -> bool | None:
        """
        Check if only an inbound airport transfer has been requested.
        
        Returns:
            True if only an inbound transfer has been requested, False otherwise
        """
        return self._get('airportTransferInboundOnly')
    
    @airportTransferInboundOnly.setter
    def airportTransferInboundOnly(self, value: bool) -> None:
        """
        Set whether only an inbound airport transfer has been requested.
        
        Args:
            value: True if only an inbound transfer has been requested
        """
        self._set('airportTransferInboundOnly', value)

    @property
    def airportTransferOutboundOnly(self) -> bool | None:
        """
        Check if only an outbound airport transfer has been requested.
        
        Returns:
            True if only an outbound transfer has been requested, False otherwise
        """
        return self._get('airportTransferOutboundOnly')
    
    @airportTransferOutboundOnly.setter
    def airportTransferOutboundOnly(self, value: bool) -> None:
        """
        Set whether only an outbound airport transfer has been requested.
        
        Args:
            value: True if only an outbound transfer has been requested
        """
        self._set('airportTransferOutboundOnly', value)

    @property
    def childSeats(self) -> int | None:
        """
        Get the number of child seats requested for transport.
        
        Returns:
            Number of child seats requested
        """
        return self._get('childSeats')
    
    @childSeats.setter
    def childSeats(self, value: int | None) -> None:
        """
        Set the number of child seats requested for transport.
        
        Args:
            value: Number of child seats to request
        """
        self._set('childSeats', value)

    @property
    def excessBaggage(self) -> bool | None:
        """
        Check if excess baggage capacity has been requested for transport.
        
        Returns:
            True if excess baggage capacity has been requested, False otherwise
        """
        return self._get('excessBaggage')
    
    @excessBaggage.setter
    def excessBaggage(self, value: bool) -> None:
        """
        Set whether excess baggage capacity has been requested for transport.
        
        Args:
            value: True if excess baggage capacity has been requested
        """
        self._set('excessBaggage', value)

    @property
    def ownerIsPaying(self) -> bool | None:
        """
        Check if the owner is paying for extras.
        
        Returns:
            True if the owner is paying for extras, False otherwise
        """
        return self._get('ownerIsPaying')

    @ownerIsPaying.setter
    def ownerIsPaying(self, value: bool) -> None:
        """
        Set whether the owner is paying for extras.
        
        Args:
            value: True if the owner is paying for extras
        """
        self._set('ownerIsPaying', value)

    # Calculated properties
    @property
    def arrival(self) -> list[str]:
        """
        Get a list of all extras needed at arrival.
        
        Returns:
            List of arrival extras descriptions
        """
        arrivalExtras = list()
        if self.airportTransfers or self.airportTransferInboundOnly:
            arrivalExtras.append('Airport Transfer')
        if self.cot and self.highChair:
            arrivalExtras.append('Cot & High Chair')
        elif self.cot:
            arrivalExtras.append('Cot')
        elif self.highChair:
            arrivalExtras.append('High Chair')
        if self.welcomePack:
            string = 'Welcome Pack'
            if self.welcomePackModifications:
                string += f' ({self.welcomePackModifications})' 
            arrivalExtras.append(string)
        if self.midStayClean:
            arrivalExtras.append('Mid-Stay Clean')
        if self.extraNights:
            arrivalExtras.append('Extra Nights')
        if self.otherRequests:
            arrivalExtras.append(self.otherRequests)
        return arrivalExtras
    
    @property
    def departure(self) -> list[str]:
        """
        Get a list of all extras needed at departure.
        
        Returns:
            List of departure extras descriptions
        """
        departureExtras = list()
        if self.airportTransfers or self.airportTransferOutboundOnly:
            departureExtras.append('Airport Transfer')
        if self.lateCheckout:
            departureExtras.append('Late Check-out')
        return departureExtras
    
    @property
    def list(self) -> list[str]:
        """
        Get a comprehensive list of all extras for this booking.
        
        Returns:
            List of all extras descriptions
        """
        extrasList = list()
        if self.airportTransfers:
            extrasList.append('Airport Transfers')
        elif self.airportTransferInboundOnly:
            extrasList.append('Airport Transfer Inbound Only')
        elif self.airportTransferOutboundOnly:
            extrasList.append('Airport Transfer Outbound Only')
        if self.cot and self.highChair:
            extrasList.append('Cot & High Chair')
        elif self.cot:
            extrasList.append('Cot')
        elif self.highChair:
            extrasList.append('High Chair')
        if self.welcomePack:
            string = 'Welcome Pack'
            if self.welcomePackModifications:
                string += f' ({self.welcomePackModifications})' 
            extrasList.append(string)
        if self.midStayClean:
            extrasList.append('Mid-Stay Clean')
        if self.lateCheckout:
            extrasList.append('Late Check-out')
        if self.extraNights:
            extrasList.append('Extra Nights')
        if self.otherRequests:
            extrasList.append(self.otherRequests)
        return extrasList
    
    @property
    def prettyArrival(self) -> str:
        """
        Get a comma-separated string of arrival extras.
        
        Returns:
            Formatted string of arrival extras
        """
        return ', '.join(self.arrival)
    
    @property
    def prettyDeparture(self) -> str:
        """
        Get a comma-separated string of departure extras.
        
        Returns:
            Formatted string of departure extras
        """
        return ', '.join(self.departure)
    

    def __iter__(self):
        return iter(self.list)