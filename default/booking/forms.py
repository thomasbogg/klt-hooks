from libraries.database.row import Row as DatabaseRow


class Forms(DatabaseRow):
    """
    Represents form links and statuses for booking-related forms.
    
    This class manages various form URLs and completion statuses for forms that 
    guests need to complete during the booking process, including balance payment,
    guest registration, and security deposit forms.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Forms instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'forms', foreignKeys=['bookingId'])

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

    # Form URLs
    @property
    def balancePayment(self) -> str | None:
        """
        Get the URL for the balance payment form.
        Falls back to PIMS balance payment form if none is explicitly set.
        
        Returns:
            The URL to the balance payment form
        """
        value = self._get('balancePayment')
        if value is None:
            return self._pims_balance_payment()
        return value

    @balancePayment.setter
    def balancePayment(self, value: str | None) -> None:
        """
        Set the URL for the balance payment form.
        
        Args:
            value: The form URL to set
        """
        self._set('balancePayment', value)

    @property
    def guestRegistration(self) -> str | None:
        """
        Get the URL for the guest registration form.
        Falls back to PIMS guest registration form if none is explicitly set.
        
        Returns:
            The URL to the guest registration form
        """
        value = self._get('guestRegistration')
        if value is None:
            return self._pims_guest_registration()
        return value

    @guestRegistration.setter
    def guestRegistration(self, value: str | None) -> None:
        """
        Set the URL for the guest registration form.
        
        Args:
            value: The form URL to set
        """
        self._set('guestRegistration', value)

    @property
    def securityDeposit(self) -> str | None:
        """
        Get the URL for the security deposit form.
        Falls back to PIMS security deposit form if none is explicitly set.
        
        Returns:
            The URL to the security deposit form
        """
        value = self._get('securityDeposit')
        if value is None:
            return self._pims_security_deposit()
        return value

    @securityDeposit.setter
    def securityDeposit(self, value: str | None) -> None:
        """
        Set the URL for the security deposit form.
        
        Args:
            value: The form URL to set
        """
        self._set('securityDeposit', value)

    # Form statuses
    @property
    def guestRegistrationDone(self) -> bool | None:
        """
        Check if the guest registration form has been completed.
        
        Returns:
            True if the form has been completed, False otherwise
        """
        return self._get('guestRegistrationDone')

    @guestRegistrationDone.setter
    def guestRegistrationDone(self, value: bool) -> None:
        """
        Set whether the guest registration form has been completed.
        
        Args:
            value: True if the form has been completed
        """
        self._set('guestRegistrationDone', value)

    @property
    def arrivalQuestionnaire(self) -> str | None:
        """
        Get the URL for the arrival questionnaire form.
        
        Returns:
            The URL to the arrival questionnaire form
        """
        return self._get('arrivalQuestionnaire')

    @arrivalQuestionnaire.setter
    def arrivalQuestionnaire(self, value: str | None) -> None:
        """
        Set the URL for the arrival questionnaire form.
        
        Args:
            value: The form URL to set
        """
        self._set('arrivalQuestionnaire', value)

    # PIMS identifiers
    @property
    def PIMSuin(self) -> str | None:
        """
        Get the PIMS unique identifier number.
        
        Returns:
            The PIMS UIN for form generation
        """
        return self._get('PIMSuin')

    @PIMSuin.setter
    def PIMSuin(self, value: str | None) -> None:
        """
        Set the PIMS unique identifier number.
        
        Args:
            value: The PIMS UIN to set
        """
        self._set('PIMSuin', value)

    @property
    def PIMSoid(self) -> str | None:
        """
        Get the PIMS owner identifier.
        
        Returns:
            The PIMS OID for form generation
        """
        return self._get('PIMSoid')

    @PIMSoid.setter
    def PIMSoid(self, value: str | None) -> None:
        """
        Set the PIMS owner identifier.
        
        Args:
            value: The PIMS OID to set
        """
        self._set('PIMSoid', value)
    
    # Private form generation methods
    def _pims_balance_payment(self) -> str | None:
        """
        Generate a URL for the PIMS balance payment form.
        
        Returns:
            The URL to the PIMS balance payment form
        """
        return self._pims_form(num=10, formType='bookformR')
    
    def _pims_security_deposit(self) -> str | None:
        """
        Generate a URL for the PIMS security deposit form.
        
        Returns:
            The URL to the PIMS security deposit form
        """
        return self._pims_form(num=11, formType='bookformR')
    
    def _pims_guest_registration(self) -> str | None:
        """
        Generate a URL for the PIMS guest registration form.
        
        Returns:
            The URL to the PIMS guest registration form
        """
        return self._pims_form(num=6, formType='guestregR')
    
    def _pims_form(self, num: int = 0, formType: str = 'bookformR') -> str | None:
        """
        Generate a URL for a PIMS form based on the given parameters.
        
        Args:
            num: The form ID number
            formType: The type of form to generate
            
        Returns:
            The URL to the PIMS form, or None if required identifiers are missing
        """
        if not self.PIMSuin or not self.PIMSoid:
            return None
            
        prefix = 'https://www.holidayrentalbookings.com'
        formType = f'{formType}.php'
        uin = f'uin={self.PIMSuin}'
        oid = f'oid={self.PIMSoid}'
        formID = f'formID={num}'
        return f'{prefix}/{formType}?{uin}&{oid}&{formID}'