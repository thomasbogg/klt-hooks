from libraries.database.row import Row as DatabaseRow


class Emails(DatabaseRow):
    """
    Tracks the email communications sent to guests or owners during a booking lifecycle.
    
    This class maintains flags for various automated emails that are sent at different
    stages of a booking, allowing the system to track which communications have been
    delivered and which are pending.
    """
    
    def __init__(self, database: object | None = None) -> None:
        """
        Initialize a new Emails instance.
        
        Args:
            database: The database connection to use for database operations
        """
        super().__init__(database, 'emails', foreignKeys=['bookingId'])

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

    # Pre-arrival emails
    @property
    def balancePayment(self) -> bool | None:
        """
        Check if the balance payment email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('balancePayment')

    @balancePayment.setter
    def balancePayment(self, value: bool) -> None:
        """
        Set whether the balance payment email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('balancePayment', value)

    @property
    def arrivalQuestionnaire(self) -> bool | None:
        """
        Check if the arrival questionnaire email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('arrivalQuestionnaire')

    @arrivalQuestionnaire.setter
    def arrivalQuestionnaire(self, value: bool) -> None:
        """
        Set whether the arrival questionnaire email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('arrivalQuestionnaire', value)

    @property
    def securityDepositRequest(self) -> bool | None:
        """
        Check if the security deposit request email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('securityDepositRequest')

    @securityDepositRequest.setter
    def securityDepositRequest(self, value: bool) -> None:
        """
        Set whether the security deposit request email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('securityDepositRequest', value)

    @property
    def arrivalInformation(self) -> bool | None:
        """
        Check if the arrival information email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('arrivalInformation')

    @arrivalInformation.setter
    def arrivalInformation(self, value: bool) -> None:
        """
        Set whether the arrival information email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('arrivalInformation', value)

    @property
    def airportTransfers(self) -> bool | None:
        """
        Check if the airport transfers email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('airportTransfers')

    @airportTransfers.setter
    def airportTransfers(self, value: bool) -> None:
        """
        Set whether the airport transfers email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('airportTransfers', value)

    # Check-in emails
    @property
    def checkInInstructions(self) -> bool | None:
        """
        Check if the check-in instructions email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('checkInInstructions')

    @checkInInstructions.setter
    def checkInInstructions(self, value: bool) -> None:
        """
        Set whether the check-in instructions email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('checkInInstructions', value)

    @property
    def management(self) -> bool | None:
        """
        Check if the property management email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('management')

    @management.setter
    def management(self, value: bool) -> None:
        """
        Set whether the property management email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('management', value)

    @property
    def guestRegistrationForm(self) -> bool | None:
        """
        Check if the guest registration form email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('guestRegistrationForm')

    @guestRegistrationForm.setter
    def guestRegistrationForm(self, value: bool) -> None:
        """
        Set whether the guest registration form email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('guestRegistrationForm', value)

    # During-stay emails
    @property
    def finalDaysReminder(self) -> bool | None:
        """
        Check if the final days reminder email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('finalDaysReminder')

    @finalDaysReminder.setter
    def finalDaysReminder(self, value: bool) -> None:
        """
        Set whether the final days reminder email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('finalDaysReminder', value)

    # Post-departure emails
    @property
    def securityDepositReturn(self) -> bool | None:
        """
        Check if the security deposit return email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('securityDepositReturn')

    @securityDepositReturn.setter
    def securityDepositReturn(self, value: bool) -> None:
        """
        Set whether the security deposit return email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('securityDepositReturn', value)

    @property
    def goodbye(self) -> bool | None:
        """
        Check if the goodbye email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('goodbye')

    @goodbye.setter
    def goodbye(self, value: bool) -> None:
        """
        Set whether the goodbye email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('goodbye', value)

    # Owner-related emails
    @property
    def payOwner(self) -> bool | None:
        """
        Check if the owner payment notification email has been sent.
        
        Returns:
            True if the email has been sent, False otherwise
        """
        return self._get('payOwner')

    @payOwner.setter
    def payOwner(self, value: bool) -> None:
        """
        Set whether the owner payment notification email has been sent.
        
        Args:
            value: True if the email has been sent
        """
        self._set('payOwner', value)

    @property
    def guestRegistrationFormToOwner(self) -> bool | None:
        """
        Check if the guest registration form has been forwarded to the owner.
        
        Returns:
            True if the form has been forwarded, False otherwise
        """
        return self._get('guestRegistrationFormToOwner')

    @guestRegistrationFormToOwner.setter
    def guestRegistrationFormToOwner(self, value: bool) -> None:
        """
        Set whether the guest registration form has been forwarded to the owner.
        
        Args:
            value: True if the form has been forwarded
        """
        self._set('guestRegistrationFormToOwner', value)

    # Configuration
    @property
    def paused(self) -> bool | None:
        """
        Check if automated emails for this booking are paused.
        
        Returns:
            True if emails are paused, False otherwise
        """
        return self._get('paused')

    @paused.setter
    def paused(self, value: bool) -> None:
        """
        Set whether automated emails for this booking are paused.
        
        Args:
            value: True to pause emails, False to allow emails
        """
        self._set('paused', value)